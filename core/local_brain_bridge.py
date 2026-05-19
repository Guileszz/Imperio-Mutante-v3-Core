import os
import asyncio
import time
import logging
import httpx
import google.generativeai as genai
from typing import Dict, Any, Optional

logger = logging.getLogger("LOCAL-BRAIN-BRIDGE")

class LocalBrainBridge:
    def __init__(self, gemini_api_key: Optional[str] = None, ollama_url: str = "http://localhost:11434"):
        self.gemini_api_key = gemini_api_key
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
        self.ollama_url = ollama_url
        self.timeout_threshold = 3.0  # Limite de 3 segundos para o Gemini

    def _is_complex(self, prompt: str) -> bool:
        """Determina se o prompt exige maior capacidade de processamento (Gemini) ou se pode ser local (Ollama)."""
        complex_terms = ["analise", "estratégia", "síntese", "previsão", "correlação", "otimização", "complexo"]
        return len(prompt) > 500 or any(term in prompt.lower() for term in complex_terms)

    async def generate_content(self, prompt: str, model_local: str = "llama3") -> str:
        """
        Roteamento híbrido inteligente (Gemini/Ollama) baseado em complexidade e latência.
        - Tasks complexas -> Gemini (com fallback para Ollama se > 3s ou falha).
        - Tasks simples -> Ollama (com fallback para Gemini se falha).
        """
        is_complex = self._is_complex(prompt)
        
        if is_complex and self.gemini_api_key:
            logger.info("🧠 Task COMPLEXA detectada. Roteando para Gemini Cloud...")
            try:
                start_time = time.time()
                content = await self._generate_gemini(prompt)
                latency = time.time() - start_time
                
                if latency <= self.timeout_threshold:
                    return content
                
                logger.warning(f"⚠️ Latência do Gemini ({latency:.2f}s) excedeu o limite. Acionando NEURO-TOXINA (Local)...")
            except (asyncio.TimeoutError, Exception) as e:
                logger.error(f"🚨 Falha no Gemini: {type(e).__name__}. Acionando Cérebro Local...")

        # Execução via Ollama (ou fallback de Gemini)
        try:
            return await self._generate_local(prompt, model_local)
        except Exception as e:
            # Se Ollama falhar para uma task simples, tenta Gemini como último recurso
            if not is_complex and self.gemini_api_key:
                logger.warning(f"Ollama falhou para tarefa simples, tentando Gemini como reserva...")
                try:
                    return await self._generate_gemini(prompt)
                except Exception as e2:
                    return f"ERRO_SISTEMICO: IA Local e Cloud indisponíveis. Detalhe: {e2}"
            
            return f"ERRO_SISTEMICO: Falha crítica na IA Local: {e}"

    async def _generate_gemini(self, prompt: str) -> str:
        if not self.gemini_api_key:
            raise ValueError("Gemini API Key ausente.")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = await asyncio.wait_for(
            asyncio.to_thread(model.generate_content, prompt),
            timeout=self.timeout_threshold
        )
        return response.text

    async def _generate_local(self, prompt: str, model_name: str) -> str:
        logger.info(f"🧠 Processando via IA Local ({model_name}) no nó NEURO-TOXINA...")
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False
                }
            )
            if response.status_code == 200:
                result = response.json().get("response", "")
                return result.strip()
            else:
                raise Exception(f"Erro no Ollama: {response.status_code}")

    async def get_status(self) -> Dict[str, Any]:
        """Retorna o status de saúde dos cérebros (Cloud e Local)."""
        status = {
            "cloud_gemini": "configured" if self.gemini_api_key else "missing_key",
            "local_ollama": "offline",
            "models": []
        }
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.get(f"{self.ollama_url}/api/tags")
                if resp.status_code == 200:
                    status["local_ollama"] = "online"
                    status["models"] = [m["name"] for m in resp.json().get("models", [])]
        except:
            pass
        return status
