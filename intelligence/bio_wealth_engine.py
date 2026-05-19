"""
BIO-WEALTH ENGINE v4.0.0 Beta - O Orquestrador de Lucro Real.
Fusão de Shadow Oracle, Chronos e Predator Pricing para execução autônoma.
"""

import asyncio
import logging
import random
import os
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

from intelligence.shadow_market_oracle import ShadowOracle
from intelligence.chronos import Chronos
from intelligence.predator_pricing import PredatorPricing
from intelligence.wallet_manager import WalletManager
from intelligence.ancestral_memory import AncestralMemory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - BIO-WEALTH-ENGINE - %(levelname)s - %(message)s')
logger = logging.getLogger("BIO-WEALTH-ENGINE")

class BioWealthEngine:
    def __init__(self, ancestral_memory: Optional[AncestralMemory] = None, evolution_engine: Any = None, config_path: str = "config/supra_codex.json"):
        self.ancestral_memory = ancestral_memory or AncestralMemory()
        self.oracle = ShadowOracle()
        self.chronos = Chronos(self.ancestral_memory)
        self.predator = PredatorPricing()
        self.wallet = WalletManager()
        self.evolution_engine = evolution_engine
        self.config_path = config_path
        self.is_running = False
        self.strike_count = 0
        self.assets_to_monitor = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT"]
        self.settings = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return config.get("settings", {}).get("bio_wealth_strategy", {
                        "auto_strike_enabled": True,
                        "target_roi": 0.15,
                        "min_viability_threshold": 0.05,
                        "max_strike_intensity": 1.0,
                        "aggressive_mode": False,
                        "circuit_breaker_min_balance": 500.0
                    })
        except Exception as e:
            logger.error(f"Erro ao carregar settings de Bio-Wealth: {e}")
        return {
            "auto_strike_enabled": True,
            "target_roi": 0.15,
            "min_viability_threshold": 0.05,
            "max_strike_intensity": 1.0,
            "aggressive_mode": False,
            "circuit_breaker_min_balance": 500.0
        }

    def reload_settings(self):
        self.settings = self._load_settings()
        logger.info("Settings de Bio-Wealth recarregadas.")

    def calculate_real_time_roi(self) -> float:
        """Calcula o ROI em tempo real usando o WalletManager."""
        return self.wallet.calculate_roi()

    async def run_strike(self, asset: str = "BTC/USDT", intensity: float = 1.0, reason: str = "Manual Override"):
        """
        Executa o protocolo /STRIKE: Busca máxima de lucro em um ativo alvo.
        Integra a trindade de inteligência: Oráculo, Chronos e Predator.
        """
        logger.info(f"🚀 INICIANDO PROTOCOLO /STRIKE: Alvo {asset} | Intensidade {intensity}")
        logger.info(f"Motivo da Decisão: {reason}")
        
        # 1. Inteligência de Mercado (Shadow Oracle)
        market_sentiment = self.oracle.correlator.get_market_sentiment()
        if market_sentiment["news_count"] == 0:
            logger.info("Buffer do Oráculo vazio. Acionando ciclo de coleta rápida...")
            await self.oracle.run_market_cycle()
            market_sentiment = self.oracle.correlator.get_market_sentiment()
        
        sentiment_score = market_sentiment.get("score", 0.0)
        logger.info(f"Sentimento de Mercado: {market_sentiment['overall_sentiment']} (Score: {sentiment_score})")

        # 2. Predição de Viabilidade (Chronos)
        market_data = {
            "price": 65000.0 if "BTC" in asset else 3500.0 if "ETH" in asset else 150.0,
            "volatility": abs(sentiment_score) + 0.02,
            "spread": 0.001
        }
        
        viability = await self.chronos.predict_viability(asset, market_data)
        viability_score = viability.get("viability_score", 0.0)
        logger.info(f"Score de Viabilidade (Chronos): {viability_score}")

        # Limiar de execução v4.0.0 Beta
        if viability_score < 0.65:
            logger.warning(f"Protocolo /STRIKE Abortado: Viabilidade insuficiente ({viability_score})")
            return {"status": "aborted", "reason": "low_viability", "score": viability_score}

        # 3. Identificação de Gaps de Néctar (Predator Pricing)
        base_price = market_data["price"]
        spread_factor = 0.005 * intensity
        simulated_prices = {
            "Binance": base_price,
            "Uniswap": base_price * (1 + spread_factor),
            "Kraken": base_price * (1 - 0.001)
        }
        
        opportunity = await self.predator.analyze_opportunity(asset.split('/')[0], simulated_prices)
        
        if opportunity["action"] == "EXECUTE":
            # 4. Verificação de Soberania Financeira e Execução
            balances = await self.wallet.get_balances()
            # Circuit Breaker: Soberania Financeira
            min_balance = self.settings.get("circuit_breaker_min_balance", 500.0)
            if balances.get("USDT", 0) >= min_balance:
                logger.info(f"Condições Ótimas Detectadas. Executando Predação de Mercado em {asset}...")
                execution = await self.predator.execute_front_run(opportunity["opportunities"][0])
                
                if execution["status"] == "SUCCESS":
                    profit = execution["profit_realized"]
                    await self.wallet.record_profit(asset.split('/')[0], profit, "BIO-WEALTH-STRIKE")
                    self.strike_count += 1
                    
                    # Protocolo de Proteção de Lucro: Mover 40% para Cold Storage se lucro > 100 USDT
                    if profit > 100:
                        await self.wallet.request_cold_storage_transfer(asset.split('/')[0], profit * 0.4)
                    
                    # Ciclo de Aprendizado Adaptativo (DEEP-MIND)
                    self._archive_profit_experience(asset, profit, viability_score, reason)
                        
                    return {
                        "status": "success",
                        "profit_realized": profit,
                        "viability": viability_score,
                        "strike_id": self.strike_count,
                        "reason": reason
                    }
        
        return {"status": "no_opportunity", "viability": viability_score}

    def _archive_profit_experience(self, asset: str, profit: float, viability: float, reason: str):
        """
        Ciclo de Aprendizado Adaptativo: Arquiva experiências de lucro real para refinar decisões futuras.
        Implementação do Protocolo DEEP-MIND.
        """
        doc_id = f"profit_exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(100, 999)}"
        experience_text = (
            f"STRIKE de sucesso em {asset}. Lucro Realizado: {profit} USDT. "
            f"Viabilidade detectada pelo Chronos: {viability:.2f}. Motivo da ação: {reason}. "
            f"Data: {datetime.now().isoformat()}"
        )
        
        metadata = {
            "type": "profit_experience",
            "asset": asset,
            "profit": profit,
            "viability_score": viability,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        try:
            self.ancestral_memory.add_knowledge(experience_text, metadata, doc_id)
            logger.info(f"✅ Experiência de lucro arquivada na Memória Ancestral (DEEP-MIND): {doc_id}")
        except Exception as e:
            logger.error(f"Erro ao arquivar experiência de lucro: {e}")

    async def start_autonomous_loop(self):
        """Loop de Riqueza Autônomo Decisório: Consulta a EvolutionEngine para agir."""
        self.is_running = True
        logger.info("🌀 BIO-WEALTH LOOP ATIVADO - Autonomia Decisória Total (/EVOLUIR).")
        
        while self.is_running:
            try:
                if self.evolution_engine:
                    roi = self.calculate_real_time_roi()
                    balances = await self.wallet.get_balances()
                    market_sentiment = self.oracle.correlator.get_market_sentiment()
                    
                    # Decisão estratégica via IA
                    decision = await self.evolution_engine.get_strike_decision(market_sentiment, roi, balances)
                    
                    if decision.get("execute"):
                        asset = decision.get("asset", "BTC/USDT")
                        intensity = decision.get("intensity", 1.0)
                        reason = decision.get("reason", "IA Decision")
                        await self.run_strike(asset, intensity, reason)
                    else:
                        logger.info(f"IA decidiu não agir. Razão: {decision.get('reason')}")
                else:
                    # Fallback para o modo aleatório se o motor de evolução não estiver presente
                    asset = random.choice(self.assets_to_monitor)
                    await self.run_strike(asset, intensity=random.uniform(0.8, 1.5), reason="Fallback Random")
                
                # Intervalo dinâmico baseado em volatilidade? Por enquanto fixo entre 30-120s
                wait_time = random.randint(30, 120)
                await asyncio.sleep(wait_time)
            except Exception as e:
                logger.error(f"Erro crítico no Bio-Wealth Loop: {e}")
                await asyncio.sleep(60)

    def stop_autonomous_loop(self):
        self.is_running = False
        logger.info("Bio-Wealth Loop desativado.")

if __name__ == "__main__":
    async def test():
        engine = BioWealthEngine()
        await engine.oracle.run_market_cycle()
        res = await engine.run_strike("BTC/USDT", intensity=2.0)
        print(res)
        
    asyncio.run(test())
