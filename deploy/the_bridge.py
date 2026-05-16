"""
THE BRIDGE v1.0 - Protocolo de Transmissão e Deploy
Gerencia o deploy de ativos para ambientes de produção (GitHub, Vercel, Docker).
"""

import os
import asyncio
import logging
import httpx
import base64
from typing import Dict, Any, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - THE-BRIDGE - %(levelname)s - %(message)s')
logger = logging.getLogger("THE-BRIDGE")

class DeploymentBridge:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_user = os.getenv("GITHUB_USER", "guitriloco")
        self.vercel_token = os.getenv("VERCEL_TOKEN")

    async def deploy_to_github(self, project_name: str, files: Dict[str, str]) -> Dict[str, Any]:
        """Faz o push dos arquivos para o GitHub."""
        logger.info(f"Iniciando deploy para GitHub: {project_name}")
        
        repo_name = project_name.lower().replace(" ", "-").replace("_", "-")
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # 1. Garantir que o repositório existe
        repo_full_name = f"{self.github_user}/{repo_name}"
        try:
            async with httpx.AsyncClient() as client:
                # Tenta criar
                create_resp = await client.post(
                    "https://api.github.com/user/repos",
                    headers=headers,
                    json={"name": repo_name, "private": True}
                )
                if create_resp.status_code == 201:
                    logger.info(f"Repositório {repo_full_name} criado.")
                elif create_resp.status_code == 422:
                    logger.info(f"Repositório {repo_full_name} já existe.")
                else:
                    return {"success": False, "error": f"Erro GitHub: {create_resp.text}"}

                # 2. Upload de arquivos
                for file_path, content in files.items():
                    url = f"https://api.github.com/repos/{repo_full_name}/contents/{file_path}"
                    
                    # Checar se existe para pegar SHA
                    sha = None
                    check_resp = await client.get(url, headers=headers)
                    if check_resp.status_code == 200:
                        sha = check_resp.json()["sha"]
                    
                    data = {
                        "message": f"The Bridge: Deploying {file_path}",
                        "content": base64.b64encode(content.encode()).decode(),
                    }
                    if sha:
                        data["sha"] = sha
                    
                    put_resp = await client.put(url, headers=headers, json=data)
                    if put_resp.status_code not in [200, 201]:
                        logger.error(f"Erro ao subir {file_path}: {put_resp.text}")

            return {"success": True, "repository": repo_full_name}
        except Exception as e:
            logger.error(f"Falha no deploy GitHub: {e}")
            return {"success": False, "error": str(e)}

    async def deploy_to_vercel(self, project_name: str, files: Dict[str, str]) -> Dict[str, Any]:
        """Simulação de deploy para Vercel (Placeholder)."""
        logger.info(f"Simulando deploy para Vercel: {project_name}")
        await asyncio.sleep(2)
        return {"success": True, "url": f"https://{project_name.lower()}.vercel.app"}

    async def rollback(self, project_name: str, version: str) -> bool:
        """Executa rollback para uma versão anterior."""
        logger.warning(f"Iniciando ROLLBACK para {project_name} (versão: {version})")
        # Lógica de rollback aqui
        return True

    async def run_pipeline(self, project_name: str, files: Dict[str, str]) -> Dict[str, Any]:
        """Executa o pipeline completo de deploy."""
        results = {}
        
        # Deploy GitHub
        github_res = await self.deploy_to_github(project_name, files)
        results["github"] = github_res
        
        if github_res["success"]:
            # Se for um web app (tem HTML ou JS), tenta Vercel
            if any(f.endswith((".html", ".js", ".jsx", ".tsx")) for f in files.keys()):
                vercel_res = await self.deploy_to_vercel(project_name, files)
                results["vercel"] = vercel_res
        
        return results
