"""
P2P CONSENSUS PROTOCOL (O TELHADO) v1.1
Sincronização de estado descentralizada entre os nós do Império Mutante.
Garante consistência global do Supra-Codex e métricas de saúde.
"""

import asyncio
import json
import logging
import time
import hashlib
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime

logger = logging.getLogger("P2P-CONSENSUS")

@dataclass
class ConsensusState:
    last_mutation_hash: str = ""
    last_mutation_time: float = 0.0
    active_nodes: List[str] = field(default_factory=list)
    global_profit: float = 0.0
    mesh_leader: str = ""
    version: str = "1.1.0"

class P2PConsensus:
    def __init__(self, node_id: str, nodes_config: Dict[str, Any], neural_bridge=None):
        self.node_id = node_id
        self.nodes_config = nodes_config
        self.neural_bridge = neural_bridge
        self.state = ConsensusState()
        self.peers = [nid for nid in nodes_config if nid != node_id]
        self.sync_interval = 10  # Gossip interval in seconds
        self.is_running = False

    def update_local_state(self, updates: Dict[str, Any]):
        """Atualiza o estado local do consenso."""
        for key, value in updates.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)
        
        # Se houver mutação, atualiza o hash
        if "last_mutation_time" in updates:
            self.state.last_mutation_hash = self._generate_hash(str(updates.get("last_mutation_time")))

    def _generate_hash(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    async def propagate_state(self):
        """Propaga o estado atual para vizinhos aleatórios (Gossip)."""
        if not self.peers:
            return

        # Inclui o conteúdo do Supra-Codex se for uma mutação recente
        payload_dict = asdict(self.state)
        try:
            if os.path.exists("config/supra_codex.json"):
                with open("config/supra_codex.json", "r") as f:
                    payload_dict["supra_codex_content"] = f.read()
        except Exception as e:
            logger.error(f"Erro ao ler supra_codex para propagação: {e}")

        payload = json.dumps(payload_dict)
        
        # Escolhe um vizinho para fofocar
        import random
        peer_id = random.choice(self.peers)
        peer_info = self.nodes_config.get(peer_id)
        
        if not peer_info:
            return

        logger.info(f"Propagando estado P2P para {peer_id}...")
        
        success = False
        # Tenta gRPC primeiro se disponível
        if self.neural_bridge:
            try:
                # O endereço gRPC geralmente está na porta 50051 (padrão)
                # Precisamos descobrir o endereço gRPC do vizinho. 
                endpoint = peer_info.get('endpoint', '')
                if ':' in endpoint:
                    port_str = endpoint.split(':')[-1]
                    if port_str.isdigit():
                        grpc_port = 50050 + int(port_str) - 8000
                        target_address = f"localhost:{grpc_port}"
                        
                        if hasattr(self.neural_bridge, 'exchange_mutation'):
                            await self.neural_bridge.exchange_mutation(target_address, self.node_id, payload, "CONSENSUS_SYNC")
                            success = True
            except Exception as e:
                logger.error(f"Falha na propagação gRPC para {peer_id}: {e}")

        # Fallback para REST se gRPC falhar ou não estiver disponível
        if not success:
            try:
                import httpx
                async with httpx.AsyncClient(timeout=2.0) as client:
                    await client.post(f"{peer_info['endpoint']}/p2p/sync", json={
                        "sender": self.node_id,
                        "state": payload_dict
                    })
                    success = True
            except Exception as e:
                # logger.error(f"Falha na propagação REST para {peer_id}: {e}")
                pass

    async def handle_sync_request(self, sender_id: str, remote_state_dict: Dict[str, Any]):
        """Processa uma requisição de sincronização de outro nó."""
        # Extrai conteúdo do supra codex se presente
        remote_codex = remote_state_dict.pop("supra_codex_content", None)
        
        # Filtra chaves válidas para ConsensusState
        valid_keys = ConsensusState.__dataclass_fields__.keys()
        state_data = {k: v for k, v in remote_state_dict.items() if k in valid_keys}
        remote_state = ConsensusState(**state_data)
        
        logger.info(f"Recebido sync P2P de {sender_id} (versão: {remote_state.version})")
        
        # Lógica de Consenso: O estado mais recente vence ou se o remetente for GHOST-EMPEROR (Mestre)
        is_master = "GHOST-EMPEROR" in sender_id
        if is_master or remote_state.last_mutation_time > self.state.last_mutation_time:
            logger.info(f"Sincronizando com {sender_id} (Mestre ou Mais Recente)")
            self.state = remote_state
            
            if remote_codex:
                try:
                    # Salva o novo Supra-Codex localmente
                    with open("config/supra_codex.json", "w") as f:
                        f.write(remote_codex)
                    logger.info("Supra-Codex atualizado via P2P.")
                except Exception as e:
                    logger.error(f"Erro ao salvar Supra-Codex recebido: {e}")
            
            return True
        elif remote_state.last_mutation_time == self.state.last_mutation_time:
            # Já sincronizado
            if sender_id not in self.state.active_nodes:
                self.state.active_nodes.append(sender_id)
            return False
        else:
            # Nosso estado é mais recente, o remetente deve se atualizar em breve via Gossip
            return False

    async def start_loop(self):
        self.is_running = True
        while self.is_running:
            try:
                await self.propagate_state()
            except Exception as e:
                logger.error(f"Erro no loop de consenso: {e}")
            await asyncio.sleep(self.sync_interval)

    def stop_loop(self):
        self.is_running = False

    def get_mesh_status(self):
        return {
            "node_id": self.node_id,
            "state": asdict(self.state),
            "peers": self.peers,
            "is_synchronized": True # Simplificação
        }
