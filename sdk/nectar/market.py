"""
SOVEREIGN INTELLIGENCE SDK - NECTAR MARKET
Predação de Mercado Distilada.
"""

import asyncio
import logging
from ..core.pricing import PredatorPricing
from ..internal.oracle import ShadowMarketOracle

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [SOVEREIGN-SDK] - %(levelname)s - %(message)s')
logger = logging.getLogger("SOVEREIGN-SDK-NECTAR-MARKET")

class NectarMarket:
    def __init__(self):
        self.pricing = PredatorPricing()
        self.oracle = ShadowMarketOracle()
        logger.info("NECTAR MARKET - Ativado")

    async def find_and_execute(self, asset: str, external_prices: dict):
        logger.info(f"Analisando Néctar de Mercado para {asset}...")
        opp = await self.pricing.analyze_opportunity(asset, external_prices)
        
        if opp.get("action") == "EXECUTE":
            logger.info(f"🔥 Oportunidade detectada via SDK: Spread {opp['opportunities'][0]['spread']:.4f}")
            result = await self.pricing.execute_front_run(opp["opportunities"][0])
            return result
        return {"status": "WAIT", "message": "Nenhuma margem infinita encontrada."}
