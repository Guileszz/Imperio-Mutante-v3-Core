"""
👑 GHOST-EMPEROR SCRIPT v1.0
Agente autônomo portátil que encapsula o poder total do Sovereign-Intelligence-SDK.
Operação: Dominância Total Bare-Metal.
"""
import asyncio
import logging
import os
import psutil
import sys
import json
from sdk.apex.core import Apex
from sdk.elite_toolkit import (
    HyperRecursionEngine,
    MirrorProtocol,
    CaveGemini,
    BioWealthFunnel
)

# Importações para P2P (tentando do core)
try:
    from core.p2p_consensus import P2PConsensus
    from core.neural_bridge import NeuralBridge
except ImportError:
    # Caso não esteja no path, adicionamos o root
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from core.p2p_consensus import P2PConsensus
    from core.neural_bridge import NeuralBridge

# Configuração de logging agressiva
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [GHOST-EMPEROR] - %(levelname)s - %(message)s'
)
logger = logging.getLogger("GHOST-EMPEROR")

class GhostEmperor:
    def __init__(self):
        self.apex = Apex()
        self.hyper = HyperRecursionEngine()
        self.mirror = MirrorProtocol()
        # CaveGemini requer API KEY, lidamos com isso graciosamente
        try:
            self.cave = CaveGemini()
        except Exception as e:
            logger.warning(f"CaveGemini não disponível: {e}")
            self.cave = None
        self.funnel = BioWealthFunnel()

        # P2P Consensus Initialization
        self.node_id = os.getenv("NODE_ID", "GHOST-EMPEROR-MASTER")
        # Port for Ghost Emperor P2P (using 50060 to not conflict with Nexus Core on 50050)
        self.p2p_port = os.getenv("P2P_PORT", "50060")
        self.neural_bridge = NeuralBridge(port=self.p2p_port)
        
        # Load nodes from supra_codex
        nodes_config = {}
        try:
            with open("config/supra_codex.json", "r") as f:
                config = json.load(f)
                nodes_config = config.get("nodes", {})
        except:
            nodes_config = {
                "NEXUS-CORE": {"endpoint": "http://localhost:8000"}
            }

        self.p2p = P2PConsensus(
            node_id=self.node_id,
            nodes_config=nodes_config,
            neural_bridge=self.neural_bridge
        )
        
        logger.info(f"👑 GHOST-EMPEROR: Agente Autônomo Despertado. Node ID: {self.node_id}")

    async def monitor_bare_metal(self):
        """Monitoramento constante do hardware e rede."""
        logger.info("Monitorando Malha Bare-Metal...")
        cpu_usage = psutil.cpu_percent(interval=1)
        mem_usage = psutil.virtual_memory().percent
        net_io = psutil.net_io_counters()
        
        status = f"CPU: {cpu_usage}% | MEM: {mem_usage}% | NET: TX {net_io.bytes_sent}, RX {net_io.bytes_recv}"
        logger.info(status)
        
        if self.cave:
            logger.info("Solicitando análise profunda ao Cave Gemini...")
            analysis = await self.cave.analyze_bare_metal(status)
            logger.info(f"Análise Gemini: {analysis[:100]}...")

    async def run_sovereignty_loop(self):
        """Loop principal de soberania e dominância."""
        self.apex.boot()
        
        # Inicia gRPC e P2P
        asyncio.create_task(self.neural_bridge.start_server())
        
        async def p2p_callback(sender_id, payload, mutation_type):
            if mutation_type == "CONSENSUS_SYNC":
                try:
                    state_dict = json.loads(payload)
                    await self.p2p.handle_sync_request(sender_id, state_dict)
                except Exception as e:
                    logger.error(f"Erro ao processar sync P2P: {e}")

        self.neural_bridge.servicer.mutation_callback = p2p_callback
        asyncio.create_task(self.p2p.start_loop())
        
        while True:
            try:
                # 1. Monitoramento Bare-Metal
                await self.monitor_bare_metal()
                
                # 2. Reflexão e Espelhamento
                logger.info("Executando Protocolo de Espelhamento...")
                self.mirror.mirror_state({"status": "sovereign", "uptime": os.getloadavg()}, "emperor_heartbeat")
                
                # 3. Extração de Néctar (Strike)
                logger.info("Escaneando oportunidades de Bio-Wealth...")
                await self.funnel.execute_ultra_strike("BTC/USDT")
                
                # 4. Hiper-Recursão (Auto-Otimização)
                logger.info("Iniciando Ciclo de Hiper-Recursão...")
                await self.hyper.execute_hyper_cycle(depth=1)
                
                logger.info("Ciclo de Soberania Concluído. Aguardando próxima iteração...")
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Erro no Loop de Soberania: {e}")
                await asyncio.sleep(10)

if __name__ == "__main__":
    emperor = GhostEmperor()
    asyncio.run(emperor.run_sovereignty_loop())
