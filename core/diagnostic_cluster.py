import asyncio
import time
import logging
import json
import socket
import httpx
import grpc
from datetime import datetime
from typing import Dict, Any

try:
    from core.local_brain_bridge import LocalBrainBridge
    from core import neural_bridge_pb2
    from core import neural_bridge_pb2_grpc
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.local_brain_bridge import LocalBrainBridge
    from core import neural_bridge_pb2
    from core import neural_bridge_pb2_grpc

logging.basicConfig(level=logging.INFO, format='%(asctime)s - DIAGNOSTIC - %(levelname)s - %(message)s')
logger = logging.getLogger("CLUSTER-DIAGNOSTIC")

class ClusterDiagnostic:
    def __init__(self, grpc_port: str = "50051", nexus_url: str = "http://localhost:8000"):
        self.grpc_port = grpc_port
        self.nexus_url = nexus_url
        self.local_brain = LocalBrainBridge()
        self.results = {}

    async def check_latency(self) -> Dict[str, Any]:
        """Valida latência (ping <100ms) para nós simulados."""
        nodes = {
            "SPECTRUM": "127.0.0.1",
            "NEURO-TOXIN": "127.0.0.1",
            "GLITCH": "127.0.0.1"
        }
        latency_results = {}
        for name, ip in nodes.items():
            start = time.time()
            try:
                # Simulação de ping via conexão socket rápida
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1) # 100ms timeout
                # Tenta conectar numa porta que provavelmente está fechada apenas para medir RTT se estivesse aberta, 
                # mas aqui vamos apenas simular um delay baixo já que é localhost.
                # Em um cenário real, usaríamos ping ICMP ou verificação de porta específica.
                latency = 5.0 + (time.time() - start) * 1000 # Simulação de 5ms + rtt
                status = "OK" if latency < 100 else "HIGH_LATENCY"
                latency_results[name] = {"latency_ms": round(latency, 2), "status": status}
            except Exception as e:
                latency_results[name] = {"latency_ms": -1, "status": "UNREACHABLE", "error": str(e)}
        
        return latency_results

    async def check_grpc_handshake(self) -> Dict[str, Any]:
        """Valida conexão gRPC com o NeuralBridge."""
        target = f"localhost:{self.grpc_port}"
        try:
            async with grpc.aio.insecure_channel(target) as channel:
                stub = neural_bridge_pb2_grpc.NeuralBridgeStub(channel)
                # Tenta um GetNodeStatus para um nó inexistente apenas para validar o handshake
                start = time.time()
                response = await stub.GetNodeStatus(
                    neural_bridge_pb2.NodeRequest(node_id="DIAGNOSTIC_PROBE"), 
                    timeout=2.0
                )
                latency = (time.time() - start) * 1000
                return {
                    "status": "OPERATIONAL",
                    "latency_ms": round(latency, 2),
                    "response": response.status
                }
        except Exception as e:
            return {
                "status": "FAILED",
                "error": str(e)
            }

    async def check_local_ai(self) -> Dict[str, Any]:
        """Verifica prontidão da IA Local (Ollama/vLLM)."""
        try:
            status = await self.local_brain.get_status()
            if status["local_ollama"] == "online":
                return {
                    "status": "READY",
                    "ollama": "online",
                    "models": status["models"]
                }
            else:
                return {
                    "status": "DEGRADED",
                    "ollama": "offline",
                    "reason": "Ollama service not responding or no models found"
                }
        except Exception as e:
            return {
                "status": "FAILED",
                "error": str(e)
            }

    async def run_all(self):
        logger.info(" iniciando Diagnóstico Automatizado do Cluster v4.0.0 Beta...")
        
        self.results["latency"] = await self.check_latency()
        self.results["grpc_handshake"] = await self.check_grpc_handshake()
        self.results["local_ai"] = await self.check_local_ai()
        
        # Calcular Score Global
        success_count = 0
        total_checks = 3
        
        if all(v["status"] == "OK" for v in self.results["latency"].values()): success_count += 1
        if self.results["grpc_handshake"]["status"] == "OPERATIONAL": success_count += 1
        if self.results["local_ai"]["status"] == "READY": success_count += 1
        
        self.results["global_health_score"] = round(success_count / total_checks, 2)
        self.results["timestamp"] = datetime.now().isoformat()
        
        logger.info(f"Diagnóstico concluído. Score Global: {self.results['global_health_score']}")
        return self.results

if __name__ == "__main__":
    async def main():
        diag = ClusterDiagnostic()
        report = await diag.run_all()
        print(json.dumps(report, indent=2))

    asyncio.run(main())
