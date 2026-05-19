"""
HARVEST MANAGER v1.0 - Orquestrador de Busca e Extração Soberana.
Consolida ShadowOracle, ShadowCrawler e ZenithAutomation sob um único comando.
"""

import asyncio
import logging
import random
from typing import List, Dict, Any, Optional

from intelligence.shadow_market_oracle import ShadowOracle
from intelligence.shadow_crawler import ShadowCrawler
from intelligence.zenith_automation import ZenithEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - HARVEST-MANAGER - %(levelname)s - %(message)s')
logger = logging.getLogger("HARVEST-MANAGER")

class HarvestManager:
    def __init__(self, nexus_endpoint: str = "http://localhost:8000"):
        self.nexus_endpoint = nexus_endpoint
        self.oracle = ShadowOracle(alquimia_endpoint=nexus_endpoint)
        self.crawler = ShadowCrawler(neuro_toxin_endpoint=f"{nexus_endpoint}/ingress")
        self.zenith = ZenithEngine(alquimia_endpoint=nexus_endpoint)
        
        self.is_running = False

    async def start_harvest_loop(self):
        """Inicia todos os serviços de coleta em paralelo."""
        self.is_running = True
        logger.info("Iniciando Orquestrador de Colheita (HarvestManager)...")
        
        tasks = [
            self.oracle.run_cycle(),
            self.crawler.run_cycle(),
            self.run_zenith_loop()
        ]
        
        await asyncio.gather(*tasks)

    async def run_zenith_loop(self):
        """Zenith não tem um run_cycle nativo similar aos outros, criamos um."""
        while self.is_running:
            try:
                logger.info("Zenith: Iniciando ciclo de extração recursiva...")
                await self.zenith.harvest_nectar()
                wait_time = random.uniform(300, 600)
                logger.info(f"Zenith: Ciclo concluído. Próxima extração em {wait_time:.1f}s.")
                await asyncio.sleep(wait_time)
            except Exception as e:
                logger.error(f"Erro no loop do Zenith: {e}")
                await asyncio.sleep(60)

    async def stop(self):
        self.is_running = False
        await self.oracle.close()
        await self.zenith.close()
        # ShadowCrawler uses a shared client that is closed on each request or has its own management

if __name__ == "__main__":
    manager = HarvestManager()
    try:
        asyncio.run(manager.start_harvest_loop())
    except KeyboardInterrupt:
        logger.info("HarvestManager encerrado pelo operador.")
