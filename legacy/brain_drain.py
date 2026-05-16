"""
BRAIN DRAIN v1.0 - Destilador de Ideias Legadas.
Extrai capital intelectual de arquivos brutos e transforma em planos de execução estruturados.

ARQUITETURA:
├── Scanner (Varredura de /legacy)
├── Distiller (Gemini-powered synthesis)
└── Injector (Integração com Alquimia)
"""

import os
import asyncio
import json
import logging
import glob
import httpx
from typing import List, Dict, Any
from datetime import datetime

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - BRAIN-DRAIN - %(levelname)s - %(message)s')
logger = logging.getLogger("BRAIN-DRAIN")

class BrainDrain:
    def __init__(self, legacy_dir: str = "legacy", alquimia_endpoint: str = "http://localhost:8001"):
        self.legacy_dir = legacy_dir
        self.alquimia_endpoint = alquimia_endpoint
        
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            logger.warning("GEMINI_API_KEY não encontrada.")

    def scan_legacy_files(self) -> List[str]:
        """Varre o diretório legacy por arquivos .txt."""
        pattern = os.path.join(self.legacy_dir, "*.txt")
        return glob.glob(pattern)

    async def distill_idea(self, file_path: str) -> Dict[str, Any]:
        """
        Usa Gemini para transformar texto bruto em um plano de execução estruturado.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()
            
            if not raw_content.strip():
                return None

            logger.info(f"Destilando poder de: {file_path}")
            
            prompt = f"""[SISTEMA: BRAIN DRAIN - DESTILAÇÃO DE PODER]
Transforme o texto legado abaixo em um Plano de Execução Estruturado para o Império Mutante.

TEXTO LEGADO:
\"\"\"
{raw_content}
\"\"\"

O plano deve conter:
1. Objetivo (O que queremos alcançar)
2. Estratégia (O 'como' em alto nível)
3. Tática (Passos práticos de implementação)
4. KPIs (Como mediremos o sucesso)

SAÍDA FORMATADA EM MARKDOWN.
"""
            if not self.model:
                return {"file": file_path, "content": "Gemini indisponível", "status": "error"}

            response = await asyncio.to_thread(self.model.generate_content, prompt)
            return {
                "file": os.path.basename(file_path),
                "plan": response.text,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro ao destilar {file_path}: {e}")
            return None

    async def inject_to_alquimia(self, plan: Dict[str, Any]) -> bool:
        """
        Envia o plano gerado para o Knowledge Store da Alquimia.
        """
        if not plan: return False
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{self.alquimia_endpoint}/knowledge/store",
                    json={
                        "content": plan["plan"],
                        "source": f"brain_drain:{plan['file']}",
                        "tags": ["LEGACY_IDEA", "EXECUTION_PLAN"]
                    },
                    timeout=10.0
                )
                if resp.status_code == 200:
                    logger.info(f"Plano de {plan['file']} injetado na Alquimia.")
                    return True
                else:
                    logger.warning(f"Falha ao injetar na Alquimia: {resp.status_code}")
                    return False
        except Exception as e:
            logger.error(f"Erro de conexão com Alquimia: {e}")
            return False

    async def generate_business_plan(self, topic: str = None) -> Dict[str, Any]:
        """
        Gera um plano de negócio estruturado (JSON) para um Micro-SaaS ou Bot.
        """
        try:
            logger.info(f"Gerando plano de negócio para: {topic or 'Nicho Aleatório'}")
            
            prompt = f"""[SISTEMA: BRAIN DRAIN - BUSINESS PLANNER]
Gere um plano de negócio detalhado para um Micro-SaaS ou Bot lucrativo.
Foco em: Automação, IA, Web Scraping ou Ferramentas de Produtividade.

{f"TEMA ESPECÍFICO: {topic}" if topic else "NICHO: Escolha um nicho de mercado carente de automação."}

RETORNE APENAS UM JSON PURO com a seguinte estrutura:
{{
  "name": "Nome do Projeto",
  "niche": "Descrição do nicho",
  "stack": "Python/FastAPI ou Node.js",
  "features": ["feature 1", "feature 2"],
  "mvp_structure": {{
    "files": ["main.py", "requirements.txt", "Dockerfile", "README.md"],
    "description": "Explicação da arquitetura"
  }},
  "monetization": "Plano de monetização"
}}
"""
            if not self.model:
                return {"error": "Gemini indisponível"}

            response = await asyncio.to_thread(self.model.generate_content, prompt)
            content = response.text
            
            # Limpeza básica de Markdown se o Gemini teimar em colocar
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            return json.loads(content)
        except Exception as e:
            logger.error(f"Erro ao gerar plano de negócio: {e}")
            return {"error": str(e)}

    async def run(self):
        """Executa o processo completo de Brain Drain."""
        files = self.scan_legacy_files()
        if not files:
            logger.info("Nenhum arquivo legado encontrado para processar.")
            return

        logger.info(f"Encontrados {len(files)} arquivos legados.")
        
        results = []
        for f in files:
            plan = await self.distill_idea(f)
            if plan:
                success = await self.inject_to_alquimia(plan)
                results.append({"file": f, "success": success})
        
        return results

if __name__ == "__main__":
    async def main():
        drain = BrainDrain()
        results = await drain.run()
        print(results)
    
    asyncio.run(main())
