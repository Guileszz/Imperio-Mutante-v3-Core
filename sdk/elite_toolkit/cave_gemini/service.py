"""
♊ CAVE GEMINI v1.0 - O Núcleo de Inteligência Profunda.
Interface avançada para modelos generativos com foco em Bare-Metal.
"""
import os
import logging
import google.generativeai as genai
from typing import Optional

logger = logging.getLogger("SOVEREIGN-ELITE-CAVE-GEMINI")

class CaveGemini:
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY não encontrada no ambiente.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        logger.info(f"CAVE GEMINI - Túnel de Inteligência Aberto: {model_name}")

    async def analyze_bare_metal(self, system_specs: str):
        """
        Analisa o estado bare-metal e sugere otimizações extremas.
        """
        prompt = f"""[SISTEMA: CAVE GEMINI - BARE METAL ANALYSIS]
        Analise as especificações abaixo e sugira otimizações de nível kernel/hardware para dominância total.
        
        SPECS:
        {system_specs}
        """
        response = await self.model.generate_content_async(prompt)
        return response.text
