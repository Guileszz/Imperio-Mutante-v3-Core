"""
EVOLUTION ENGINE v1.0 - Motor de Evolução Autônoma do Império Mutante.
Analisa telemetria e inteligência de mercado para sugerir e aplicar mutações no arsenal.

ARQUITETURA:
├── EvolutionEngine (Orquestrador)
│   ├── collect_evolution_data (Consolida métricas e mercado)
│   ├── generate_mutation_plan (Gemini Synthesis)
│   └── apply_arsenal_mutation (Mutação do Supra-Codex)
└── Protocolo Mutação Proativa
"""

import asyncio
import json
import os
import logging
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

import google.generativeai as genai
from dotenv import load_dotenv

# Módulos internos
from core.telemetry import TelemetrySystem
from intelligence.shadow_market_oracle import ShadowOracle
from intelligence.chronos import Chronos

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - EVOLUTION - %(levelname)s - %(message)s')
logger = logging.getLogger("EVOLUTION-ENGINE")

class EvolutionEngine:
    def __init__(self, config_path: str = "legacy/supra_codex.json"):
        self.config_path = config_path
        self.telemetry = TelemetrySystem()
        self.oracle = ShadowOracle()
        self.chronos = Chronos()
        
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            logger.warning("GEMINI_API_KEY não encontrada. Evolução operando em modo degradado.")

        self.settings = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return config.get("services", {}).get("evolution_engine", {}).get("settings", {
                        "mutation_threshold": 0.7,
                        "market_relevance_weight": 0.6,
                        "evolution_cycle_interval": 3600
                    })
        except Exception as e:
            logger.error(f"Erro ao carregar settings de evolução: {e}")
        return {
            "mutation_threshold": 0.7,
            "market_relevance_weight": 0.6,
            "evolution_cycle_interval": 3600
        }

    async def collect_evolution_data(self) -> Dict[str, Any]:
        """
        Consome APIs internas e telemetria para obter o estado atual e sentimento de mercado.
        """
        logger.info("Coletando dados para evolução...")
        
        telemetry_data = self.telemetry.get_system_stats()
        
        # Simula coleta de sentimento se o oracle estiver offline ou falhar
        try:
            market_data = await self.oracle.run_market_cycle()
        except Exception as e:
            logger.warning(f"Falha ao coletar dados do Shadow Oracle: {e}")
            market_data = {"status": "offline", "market_sentiment": {"score": 0.0, "overall_sentiment": "neutral"}}

        # Coleta predições do Chronos
        try:
            chronos_predictions = await self.chronos.predict_viability("BTC/USDT", {"price": 50000, "volatility": 0.05})
        except:
            chronos_predictions = {}

        return {
            "timestamp": datetime.now().isoformat(),
            "telemetry": telemetry_data,
            "market": market_data,
            "chronos": chronos_predictions,
            "current_config": self._get_full_config()
        }

    def _get_full_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    async def generate_mutation_plan(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Prompt para o Gemini comparando o estado atual com as oportunidades de mercado.
        """
        if not self.model:
            logger.error("Gemini não configurado. Impossível gerar plano de mutação.")
            return []

        prompt = f"""[SISTEMA: EVOLUTION ENGINE v1.0]
Analise os dados abaixo e sugira mutações no Supra-Codex para otimizar a dominância do Império Mutante.

DADOS DE TELEMETRIA:
{json.dumps(data['telemetry'], indent=2)}

INTELIGÊNCIA DE MERCADO:
{json.dumps(data['market'], indent=2)}

PREDIÇÕES CHRONOS (Viabilidade de Lucro):
{json.dumps(data['chronos'], indent=2)}

CONFIGURAÇÃO ATUAL (Resumo):
{json.dumps(data['current_config'].get('settings', {}), indent=2)}

OBJETIVO:
Sugerir novos parâmetros para 'settings' ou 'nodes' no supra_codex.json que aumentem a eficiência baseada no sentimento de mercado e na carga do sistema.
Se o mercado estiver 'bullish', aumente a agressividade (ex: reduzir delays, aumentar pesos de nós potentes).
Se a carga estiver alta, otimize thresholds de latência.

FORMATO DE SAÍDA (JSON APENAS):
[
  {{
    "parameter": "settings.latency_threshold",
    "old_value": 2.5,
    "new_value": 2.2,
    "reason": "Explicação concisa"
  }}
]

Retorne APENAS o JSON array.
"""
        try:
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            text = response.text.strip()
            
            # Limpeza básica de markdown do Gemini
            if text.startswith("```json"):
                text = text[7:-3]
            elif text.startswith("```"):
                text = text[3:-3]
                
            return json.loads(text.strip())
        except Exception as e:
            logger.error(f"Erro ao gerar plano de mutação: {e}")
            return []

    async def apply_arsenal_mutation(self, mutations: List[Dict[str, Any]]) -> bool:
        """
        Aplica as mudanças diretamente no supra_codex.json.
        """
        if not mutations:
            logger.info("Nenhuma mutação para aplicar.")
            return False

        try:
            config = self._get_full_config()
            
            # Backup
            with open(self.config_path + ".backup", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)

            applied_count = 0
            for mut in mutations:
                param = mut.get("parameter")
                new_val = mut.get("new_value")
                
                if not param: continue
                
                # Suporta parâmetros aninhados tipo settings.latency_threshold
                parts = param.split(".")
                target = config
                for part in parts[:-1]:
                    if part not in target:
                        target[part] = {}
                    target = target[part]
                
                target[parts[-1]] = new_val
                applied_count += 1
                logger.info(f"Mutação aplicada: {param} -> {new_val} ({mut.get('reason')})")

            config["meta"]["last_updated"] = datetime.now().isoformat()
            
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"Supra-Codex atualizado com {applied_count} mutações.")
            return True
        except Exception as e:
            logger.error(f"Erro ao aplicar mutações: {e}")
            # Tentar rollback?
            return False

    async def run_cycle(self):
        """Executa um ciclo completo de evolução."""
        data = await self.collect_evolution_data()
        mutations = await self.generate_mutation_plan(data)
        if mutations:
            success = await self.apply_arsenal_mutation(mutations)
            return {"status": "success" if success else "failed", "mutations": mutations}
        return {"status": "no_changes"}

if __name__ == "__main__":
    async def test():
        engine = EvolutionEngine()
        result = await engine.run_cycle()
        print(result)
    
    asyncio.run(test())
