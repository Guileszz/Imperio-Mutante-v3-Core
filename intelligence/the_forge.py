"""
THE FORGE v1.0 - A Fábrica de Ativos do Império Mutante.
Gera código-fonte, documentação e integra com GitHub.
"""

import os
import asyncio
import json
import logging
import httpx
import base64
from typing import List, Dict, Any, Optional
from datetime import datetime

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - THE-FORGE - %(levelname)s - %(message)s')
logger = logging.getLogger("THE-FORGE")

class TheForge:
    def __init__(self, glitch_endpoint: str = "http://localhost:8003"):
        self.glitch_endpoint = glitch_endpoint
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_user = os.getenv("GITHUB_USER", "guitriloco")
        
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            logger.warning("GEMINI_API_KEY não encontrada.")

    def _clean_code(self, content: str) -> str:
        """Limpa blocos de Markdown do código gerado."""
        if "```" in content:
            parts = content.split("```")
            if len(parts) >= 3:
                code = parts[1]
                if "\n" in code:
                    first_line = code.split("\n")[0].strip().lower()
                    if first_line in ["python", "javascript", "typescript", "js", "ts", "json", "bash", "sh", "html", "css", "dockerfile", "markdown"]:
                        code = "\n".join(code.split("\n")[1:])
                return code.strip()
        return content.strip()

    async def generate_asset_code(self, plan: Dict[str, Any]) -> Dict[str, str]:
        """
        Gera o código-fonte real para os arquivos definidos no plano.
        """
        if not self.model:
            return {"error": "Gemini indisponível"}

        generated_files = {}
        project_name = plan.get("name", "Unknown-Project")
        
        for file_name in plan.get("mvp_structure", {}).get("files", ["main.py", "README.md"]):
            logger.info(f"Forjando arquivo: {file_name} para {project_name}")
            
            prompt = f"""[SISTEMA: THE FORGE - ASSET GENERATOR]
Você é um desenvolvedor sênior do Império Mutante.
Gere o conteúdo para o arquivo '{file_name}' do projeto '{project_name}'.

PLANO DE NEGÓCIO:
{json.dumps(plan, indent=2)}

REGRAS:
- Código pronto para produção.
- Se for Python, use FastAPI se apropriado.
- Inclua comentários mínimos e eficientes.
- RETORNE APENAS O CONTEÚDO BRUTO DO ARQUIVO.
"""
            try:
                response = await asyncio.to_thread(self.model.generate_content, prompt)
                generated_files[file_name] = self._clean_code(response.text)
            except Exception as e:
                logger.error(f"Erro ao gerar {file_name}: {e}")
        
        return generated_files

    async def create_github_repo(self, project_name: str) -> Optional[str]:
        """
        Cria um repositório privado no GitHub.
        """
        if not self.github_token:
            logger.warning("GITHUB_TOKEN não encontrado. Pulando criação de repo.")
            return None

        repo_name = project_name.lower().replace(" ", "-").replace("_", "-")
        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "name": repo_name,
            "private": True,
            "description": f"Ativo gerado automaticamente pelo Império Mutante: {project_name}"
        }

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, headers=headers, json=data)
                if resp.status_code == 201:
                    logger.info(f"Repositório {repo_name} criado com sucesso.")
                    return resp.json()["full_name"]
                elif resp.status_code == 422:
                    logger.info(f"Repositório {repo_name} já existe.")
                    return f"{self.github_user}/{repo_name}"
                else:
                    logger.error(f"Erro ao criar repo no GitHub: {resp.status_code} - {resp.text}")
                    return None
        except Exception as e:
            logger.error(f"Erro de conexão com GitHub: {e}")
            return None

    async def upload_to_github(self, repo_full_name: str, files: Dict[str, str]):
        """
        Faz o upload dos arquivos para o repositório via API de Contents.
        """
        if not self.github_token or not repo_full_name:
            return

        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        for file_path, content in files.items():
            url = f"https://api.github.com/repos/{repo_full_name}/contents/{file_path}"
            
            # Precisamos do SHA se o arquivo já existir (para update)
            sha = None
            async with httpx.AsyncClient() as client:
                check_resp = await client.get(url, headers=headers)
                if check_resp.status_code == 200:
                    sha = check_resp.json()["sha"]

            data = {
                "message": f"Forge: Gerando {file_path}",
                "content": base64.b64encode(content.encode()).decode(),
            }
            if sha:
                data["sha"] = sha

            async with httpx.AsyncClient() as client:
                resp = await client.put(url, headers=headers, json=data)
                if resp.status_code in [200, 201]:
                    logger.info(f"Arquivo {file_path} enviado para {repo_full_name}.")
                else:
                    logger.error(f"Erro ao enviar {file_path}: {resp.status_code} - {resp.text}")

    async def signal_glitch_deploy(self, repo_full_name: str, project_name: str):
        """
        Notifica o nó GLITCH para realizar o deploy.
        """
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "action": "deploy",
                    "repo": repo_full_name,
                    "project": project_name,
                    "timestamp": datetime.now().isoformat()
                }
                resp = await client.post(f"{self.glitch_endpoint}/process", json=payload, timeout=5.0)
                if resp.status_code == 200:
                    logger.info(f"Nó GLITCH notificado para deploy de {project_name}.")
                    return True
        except Exception as e:
            logger.warning(f"Não foi possível notificar o nó GLITCH: {e}")
        return False

    async def forjar(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera os arquivos do ativo baseado no plano.
        """
        if "error" in plan:
            return plan

        project_name = plan.get("name", "Asset")
        
        # 1. Gerar Código
        files = await self.generate_asset_code(plan)
        if "error" in files:
            return files

        return {
            "status": "success",
            "project": project_name,
            "files": files,
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Teste rápido se executado diretamente
    async def test():
        forge = TheForge()
        test_plan = {
            "name": "Forge Test Bot",
            "mvp_structure": {"files": ["bot.py", "README.md"]}
        }
        result = await forge.forjar(test_plan)
        print(result)
    
    # asyncio.run(test())
    pass
