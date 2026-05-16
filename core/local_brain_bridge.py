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

    async def generate_content(self, prompt: str, model_local: str = "llama3") -> str:
        """
        Tenta gerar conteúdo usando Gemini (Cloud).
        Se a latência for > 3s ou houver falha, faz fallback automático para Ollama (Local).
        """
        if self.gemini_api_key:
            try:
                start_time = time.time()
                # Tenta Gemini com timeout estrito
                content = await self._generate_gemini(prompt)
                latency = time.time() - start_time
                
                if latency > self.timeout_threshold:
                    logger.warning(f"⚠️ Latência do Gemini ({latency:.2f}s) excedeu o limite de {self.timeout_threshold}s.")
                    # Poderíamos forçar o fallback aqui, mas o _generate_gemini já deve ter retornado se não deu timeout.
                    # No entanto, a regra diz: "se a latência for > 3s... redireciona".
                    # Se o _generate_gemini demorou 4s mas não deu timeout no wait_for, ainda queremos fallback para a próxima ou essa?
                    # O wait_for(timeout=3.0) já garante que se passar de 3s ele lança TimeoutError.
                
                return content
            except (asyncio.TimeoutError, Exception) as e:
                logger.error(f"🚨 Falha ou latência excessiva no Gemini: {type(e).__name__}. Acionando Cérebro Local (NEURO-TOXINA)...")
        
        # Fallback para IA Local (Ollama)
        return await self._generate_local(prompt, model_local)

    async def _generate_gemini(self, prompt: str) -> str:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = await asyncio.wait_for(
            asyncio.to_thread(model.generate_content, prompt),
            timeout=self.timeout_threshold
        )
        return response.text

    async def _generate_local(self, prompt: str, model_name: str) -> str:
        logger.info(f"🧠 Processando via IA Local ({model_name}) no nó NEURO-TOXINA...")
        try:
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
                    # Limpeza básica de tags markdown se houver
                    return result.strip()
                else:
                    return f"Erro no Ollama: {response.status_code} - {response.text}"
        except Exception as e:
            logger.error(f"❌ Falha crítica ao conectar com Ollama: {e}")
            return f"ERRO_SISTEMICO: IA Local e Cloud indisponíveis. Detalhe: {e}"

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
