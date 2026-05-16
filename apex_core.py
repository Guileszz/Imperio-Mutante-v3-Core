"""
🚀 APEX CORE v4.0.0 - O Ápice da Soberania Computacional
Este é o orquestrador supremo que consolida todos os avanços do Império Mutante.
"""
import sys
import os
from core.nexus_core import app, logger

# Adiciona o diretório atual ao PYTHONPATH para garantir importações corretas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ApexCore:
    def __init__(self):
        self.version = "4.0.0-APEX"
        logger.info(f"APEX CORE v{self.version} Inicializado.")

    def run(self):
        import uvicorn
        logger.info("Iniciando o Império no modo SOBERANIA TOTAL...")
        uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    apex = ApexCore()
    apex.run()
