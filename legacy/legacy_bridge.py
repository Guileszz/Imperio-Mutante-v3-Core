"""
LEGACY BRIDGE - Império Mutante
Interoperabilidade entre scripts v2.5.0 (Trindade) e NEXUS CORE v3.2.0.
Redireciona tráfego legado para a nova infraestrutura soberana.
"""

import os
import httpx
import logging
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Optional, Any, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LEGACY-BRIDGE")

app = FastAPI(title="Imperio Mutante Legacy Bridge", version="1.0.0")

NEXUS_URL = os.getenv("NEXUS_URL", "http://localhost:8000")

class LegacyIngressRequest(BaseModel):
    content: Union[str, Dict[str, Any]]
    priority: Optional[str] = None
    metadata: Optional[Dict] = {}

@app.post("/ingress")
async def legacy_ingress(request: LegacyIngressRequest):
    """Mapeia o antigo /ingress para o novo NEXUS CORE."""
    logger.info(f"Recebida requisição legada para /ingress")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{NEXUS_URL}/ingress",
                json={
                    "content": request.content,
                    "priority": request.priority,
                    "metadata": {**request.metadata, "bridge": "legacy_v2.5"}
                },
                timeout=10.0
            )
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao redirecionar para NEXUS: {e}")
            raise HTTPException(status_code=502, detail="Nexus Core inacessível via Bridge")

@app.get("/status/{task_id}")
async def legacy_status(task_id: str):
    """Consulta status no novo Nexus Core."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{NEXUS_URL}/status/{task_id}")
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada no Nexus")

@app.get("/health")
async def legacy_health():
    """Retorna o estado da ponte e do Nexus."""
    async with httpx.AsyncClient() as client:
        try:
            nexus_health = await client.get(f"{NEXUS_URL}/health")
            return {
                "bridge_status": "operational",
                "nexus_status": nexus_health.json()
            }
        except:
            return {"bridge_status": "operational", "nexus_status": "offline"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
