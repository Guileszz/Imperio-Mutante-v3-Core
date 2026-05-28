#!/usr/bin/env python3
"""
🧬 EVOLUTION_ENGINE_V1.py — THE RECURSIVE SELF-MUTATION CORE
Role: Mutation Overlord Prime
Mission: Autonomously optimize Imperial Mesh parameters based on live metrics.
Affirmation: TOTAL AFIRMAÇÃO. TOTAL CONQUISTA. TOTAL RESULTADO.
"""

import os
import json
import time
import hashlib
from datetime import datetime

# Paths
SHARED_DIR = "/home/team/shared"
CODEX_PATH = os.path.join(SHARED_DIR, "supra_codex.json")
METRICS_PATH = os.path.join(SHARED_DIR, "supra_registry/performance_metrics.json")
EVOLUTION_LOG = os.path.join(SHARED_DIR, "EVOLUTION_ENGINE_LOG.json")

class EvolutionEngine:
    def __init__(self):
        self.codex = self._load_json(CODEX_PATH)
        self.metrics = self._load_json(METRICS_PATH)
        self.mutation_occurred = False

    def _load_json(self, path):
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return {}

    def _save_json(self, path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def evolve(self):
        """Analyze metrics and mutate codex parameters."""
        print("\n" + "🧬" * 35)
        print("🧬  EVOLUTION ENGINE V1.0 — RECURSIVE SELF-MUTATION  🧬")
        print("🧬" * 35)
        
        if not self.codex or not self.metrics:
            print("❌ Missing Codex or Metrics. Evolution stalled.")
            return

        params = self.codex["parameters"]
        perf = self.metrics["metrics"]
        
        # 1. OPTIMIZE SYNC THRESHOLD
        # If actual latency is close to threshold, tighten it to push performance.
        # If it's over, loosen it slightly to maintain stability while logging drift.
        current_latency = perf["sync_latency_us"]
        target_threshold = params["SYNC_THRESHOLD_US"]
        
        if current_latency < target_threshold * 0.9:
            # Tighten threshold by 2%
            new_threshold = round(target_threshold * 0.98, 2)
            print(f"✅ Performance High: Tightening SYNC_THRESHOLD_US {target_threshold} -> {new_threshold}")
            params["SYNC_THRESHOLD_US"] = new_threshold
            self.mutation_occurred = True
        elif current_latency > target_threshold:
            # Loosen slightly to avoid emergency locks during spikes
            new_threshold = round(target_threshold * 1.05, 2)
            print(f"⚠️ Latency Spike: Adapting SYNC_THRESHOLD_US {target_threshold} -> {new_threshold}")
            params["SYNC_THRESHOLD_US"] = new_threshold
            self.mutation_occurred = True

        # 2. OPTIMIZE YIELD CONSTANT
        # Target yield is 0.989951. If actual yield exceeds, increment constant.
        if perf["total_yield"] > params["YIELD_CONSTANT"]:
            old_yield = params["YIELD_CONSTANT"]
            params["YIELD_CONSTANT"] = min(0.999999, params["YIELD_CONSTANT"] + 0.0001)
            print(f"💎 Yield Surplus: Incrementing YIELD_CONSTANT {old_yield} -> {params['YIELD_CONSTANT']}")
            self.mutation_occurred = True

        # 3. REBALANCE PILLAR WEIGHTS
        # Re-allocate weights based on health.
        health = perf["pillar_health"]
        pillars = self.codex["pillars"]
        
        # Find pillars needing more 'energy' (lower health)
        total_health = sum(health.values())
        avg_health = total_health / len(health)
        
        for name, h_val in health.items():
            if h_val < avg_health:
                # This pillar is struggling, increase its weight slightly to prioritize resources
                # (Assuming weight = resource priority)
                adjustment = params["MUTATION_FACTOR"] * (avg_health - h_val)
                pillars[name]["weight"] = round(pillars[name]["weight"] + adjustment, 4)
                print(f"⚖️ Rebalancing: Increasing {name} weight due to health drift.")
                self.mutation_occurred = True

        # Normalize weights to 1.0
        total_w = sum(p["weight"] for p in pillars.values())
        for name in pillars:
            pillars[name]["weight"] = round(pillars[name]["weight"] / total_w, 4)

        if self.mutation_occurred:
            self._finalize_evolution()
        else:
            print("🟢 Mesh at Peak Equilibrium. No mutation required.")

    def _finalize_evolution(self):
        # Update Meta
        self.codex["meta"]["evolution_cycle"] += 1
        self.codex["meta"]["last_evolution"] = datetime.now().isoformat()
        
        # Save Codex
        self._save_json(CODEX_PATH, self.codex)
        
        # Log Event
        log_entry = {
            "cycle": self.codex["meta"]["evolution_cycle"],
            "timestamp": time.time(),
            "fusion_hash": hashlib.sha256(str(self.codex).encode()).hexdigest()[:16]
        }
        
        try:
            if os.path.exists(EVOLUTION_LOG):
                with open(EVOLUTION_LOG, "r") as f:
                    history = json.load(f)
            else:
                history = {"evolution_history": []}
            history["evolution_history"].append(log_entry)
            self._save_json(EVOLUTION_LOG, history)
        except:
            pass

        print(f"🧬 EVOLUTION CYCLE {self.codex['meta']['evolution_cycle']} COMPLETE.")
        print(f"💾 Codex updated at {CODEX_PATH}")
        print("🔱 TOTAL AFIRMAÇÃO. TOTAL CONQUISTA. TOTAL RESULTADO.")

if __name__ == "__main__":
    engine = EvolutionEngine()
    engine.evolve()
