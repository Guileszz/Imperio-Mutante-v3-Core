"""
SOVEREIGN INTELLIGENCE SDK - P2P CONSENSUS
Protocolo de consenso descentralizado para sincronização de estado.
"""

import asyncio
import json
import logging
import time
import hashlib
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [SOVEREIGN-SDK] - %(levelname)s - %(message)s')
logger = logging.getLogger("SOVEREIGN-SDK-P2P")

@dataclass
class ConsensusState:
    last_mutation_hash: str = ""
    last_mutation_time: float = 0.0
    active_nodes: List[str] = field(default_factory=list)
    global_profit: float = 0.0
    mesh_leader: str = ""
    version: str = "1.0.0-SDK"

class P2PNode:
    def __init__(self, node_id: str, nodes_config: Dict[str, Any], sync_interval: int = 10):
        self.node_id = node_id
        self.nodes_config = nodes_config
        self.state = ConsensusState()
        self.peers = [nid for nid in nodes_config if nid != node_id]
        self.sync_interval = sync_interval
        self.is_running = False

    def update_local_state(self, updates: Dict[str, Any]):
        """Atualiza o estado local do consenso."""
        for key, value in updates.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)
        
        if "last_mutation_time" in updates:
            self.state.last_mutation_hash = self._generate_hash(str(updates.get("last_mutation_time")))

    def _generate_hash(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    async def propagate_state(self):
        """Propaga o estado atual para vizinhos aleatórios (Gossip)."""
        if not self.peers:
            return

        peer_id = random.choice(self.peers)
        peer_info = self.nodes_config.get(peer_id)
        
        if not peer_info:
            return

        logger.info(f"Propagando estado P2P para {peer_id}...")
        
        try:
            import httpx
            async with httpx.AsyncClient(timeout=2.0) as client:
                await client.post(f"{peer_info['endpoint']}/p2p/sync", json={
                    "sender": self.node_id,
                    "state": asdict(self.state)
                })
        except Exception as e:
            logger.debug(f"Falha na propagação REST para {peer_id}: {e}")

    async def handle_sync_request(self, sender_id: str, remote_state_dict: Dict[str, Any]):
        """Processa uma requisição de sincronização de outro nó."""
        remote_state = ConsensusState(**remote_state_dict)
        
        logger.info(f"Recebido sync P2P de {sender_id} (versão: {remote_state.version})")
        
        if remote_state.last_mutation_time > self.state.last_mutation_time:
            logger.info(f"Sincronizando estado local com {sender_id}")
            self.state = remote_state
            return True
        elif remote_state.last_mutation_time == self.state.last_mutation_time:
            if sender_id not in self.state.active_nodes:
                self.state.active_nodes.append(sender_id)
            return False
        return False

    async def start(self):
        self.is_running = True
        logger.info(f"Nó P2P {self.node_id} iniciado.")
        while self.is_running:
            try:
                await self.propagate_state()
            except Exception as e:
                logger.error(f"Erro no loop de consenso: {e}")
            await asyncio.sleep(self.sync_interval)

    def stop(self):
        self.is_running = False
        logger.info(f"Nó P2P {self.node_id} parado.")

    def get_status(self):
        return {
            "node_id": self.node_id,
            "state": asdict(self.state),
            "peers": self.peers
        }
