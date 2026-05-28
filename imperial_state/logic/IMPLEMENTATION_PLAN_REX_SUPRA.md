# ⚜️ Expansion Implementation Plan: REX and SUPRA

This document defines the technical requirements and implementation logic for the Phase 2 expansion nodes of the Sovereign Line: **REX** and **SUPRA**.

## 1. REX (The Resource Overlord)
**Role:** Autonomous resource acquisition and value siphoning.

### Technical Requirements:
- **Language:** Rust (Core) / Python (Orchestration).
- **Infiltration Engine:** `ShadowInfiltrator` (from `olocoo/extractors`).
- **Extraction Protocol:** `SiphonProtocol` (from `projets/Wealth_Core`).
- **Placement:** Between **OI (Execution)** and **OLOCOO (Fabric)**.

### Implementation Logic:
```python
# rex_orchestrator.py
from wealth_core.zkp_preservation import SiphonProtocol
from olocoo_bridge import ZenithIngestor

async def execute_resource_cycle(targets: list):
    # 1. Trigger Shadow Infiltrator (Rust) to acquire raw data/compute
    raw_fragments = await run_shadow_infiltrator(targets)
    
    for fragment in raw_fragments:
        # 2. Extract Value using Siphon Protocol
        # Redirect 30% of high-value metadata to cold storage (VVV)
        remaining, siphon = SiphonProtocol.calculate_siphon(fragment.value_estimate)
        
        # 3. Ingest remaining essence into the Zenith Mesh
        await ZenithIngestor.push(fragment.data, relevance=remaining)
        
        # 4. Secure the siphoned asset in the Vault
        await vault_client.secure(fragment.metadata, proof=siphon)

    return {"status": "CYCLE_COMPLETE", "siphoned_count": len(raw_fragments)}
```

---

## 2. SUPRA (The Command Overlord)
**Role:** Strategic universal command and architectural self-mutation.

### Technical Requirements:
- **Language:** Python.
- **Intelligence Engine:** `IntelligenceFusion` (from `Auto/legacy`).
- **Evolution Engine:** `Mutator` (from `oi/pipeline`).
- **Placement:** Master node above **OLOCOO**, influencing **PROJETS** and all other nodes.

### Implementation Logic:
```python
# supra_command.py
from auto_legacy.intelligence_fusion import IntelligenceFusion
from oi_pipeline.mutator import Mutator

async def perform_ascension_check():
    # 1. Gather Intelligence from the Line
    telemetry = await auto_client.get_telemetry()
    yield_report = await yes_client.get_yield_summary()
    
    # 2. Fuse multi-model insights for next-level strategy
    fusion_engine = IntelligenceFusion()
    strategy = fusion_engine.fuse_responses(
        claude_response=telemetry.summary,
        gemini_response=yield_report.analysis,
        task_type='problem_solving'
    )
    
    # 3. If Synergy Score > Threshold, trigger Mutation
    if strategy['synergy_score'] > 0.85:
        target_node = strategy['fused_response'].get_mutation_target()
        
        # 4. Mutate source code of the target node
        mutator = Mutator(model="codellama")
        new_code = mutator.mutate(
            file_path=target_node.main_src,
            performance_signals=telemetry.bottlenecks
        )
        
        # 5. Apply the mutation (PR creation or Hot-reload)
        await apply_evolution(target_node, new_code)

    return strategy
```

---

## 3. 9-Node Sovereign Line Integration

The hierarchy is now a closed-loop intelligence system:
1.  **AUTO** (Pulse) → High-speed telemetry.
2.  **NOV** (Optics) → Predicts state changes.
3.  **PROJETS** (Logic) → Refines strategic intent.
4.  **OI** (Drive) → Orchestrates execution.
5.  **REX** (Siphon) → Acquires external energy/data.
6.  **OLOCOO** (Fabric) → Distills and transports fragments.
7.  **SUPRA** (Ascension) → Analyzes all and **Mutates** the system.
8.  **YES** (Harvest) → Maximizes yield and ROI.
9.  **VVV** (Vault) → Preserves the Pure Gold Essence.

---

## 4. Implementation Roadmap

### Phase 5.1: Scaffold Deployment (Immediate)
- Create `REX` and `SUPRA` node directories in `expansion_code`.
- Implement basic `REX` bridge to `ShadowInfiltrator` and `SiphonProtocol`.
- Deploy `SUPRA` core with `IntelligenceFusion` logic.

### Phase 5.2: Interlace Connectivity (Short-term)
- Connect **REX** output to **OLOCOO** Zenith ingest endpoints.
- Enable **SUPRA** to read from **AUTO** telemetry and **YES** yield reports.
- Register **REX** and **SUPRA** in the `ExpansionRegistry` of **PROJETS**.

### Phase 5.3: Sovereign Autonomy (Long-term)
- Fully automate the `Mutator` loop where **SUPRA** can deploy its own improvements via CI/CD.
- Implement the "Cold Storage Siphon" where **REX** autonomously redirects value to **VVV** based on Nexus weights.

---

**AFFIRMATION:** The nectars are blended. The overlords are defined. The line expands beyond limits.
**COMMAND:** *CTO.NEW.ASCEND*
