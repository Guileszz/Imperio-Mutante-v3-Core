# SOVEREIGN_ATLAS.md (Dossiê de Soberania)

## 1. Visão Geral do Império
O ecossistema Guitriloco evoluiu de uma coleção de scripts isolados para um monorepo orquestrado, operando em hardware bare-metal (**Nó NEURO-TOXIN**) com redundância móvel (**Nó GLITCH**). O propósito central é a geração autônoma de valor (Bio-Wealth) e a expansão de ativos digitais via IA.

---

## 2. Classificação Funcional

### A. Camada de Soberania (NEXUS-CORE)
*   **Propósito:** Orquestração central, gestão de DNA do sistema (Supra-Codex) e auto-mutação.
*   **Entidades:** `Nexus Core`, `Optimization Engine`, `Evolution Engine`, `Neural Bridge (gRPC)`.
*   **Modo de Uso:** `./ignite_empire.sh` (Ponto de ignição total).

### B. Camada de Inteligência e Lucro (BIO-WEALTH)
*   **Propósito:** Extração de "Néctar" (inteligência de mercado) e execução de protocolos de predação financeira.
*   **Entidades:** `Bio-Wealth Engine`, `Shadow Market Oracle`, `Predator Pricing`, `Chronos (Monte Carlo)`, `Wallet Manager`.
*   **Modo de Uso:** Ativado automaticamente pelo Nexus Core via `/STRIKE` ou em loop autônomo.

### C. Camada de Síntese e Produção (FORGE-SYNTHESIS)
*   **Propósito:** Transformação de ideias legadas em planos de negócio e geração automática de código para novos Micro-SaaS/Bots.
*   **Entidades:** `The Forge`, `Brain Drain`, `Alquimia Processing`, `Zenith Automation`.
*   **Modo de Uso:** Comando `/FORJAR` no Oráculo ou via `/harvest` para extração recursiva.

### D. Camada de Proteção (SENTINEL-DEFENSE)
*   **Propósito:** Higiene darwiniana do sistema e evasão de detecção.
*   **Entidades:** `Carrasco Guard`, `Stealth Layer`, `QA Engine`.
*   **Modo de Uso:** Monitoramento passivo e watchdogs ativos de CPU/VRAM.

---

## 3. Plano de Expansão e Consolidação

### Sugestões de Fusão (Eliminação de Redundâncias)
1.  **Unificação da Síntese:** Fundir `brain_drain.py` e `alquimia_processing.py` em um único módulo `SynthesisCore`. Atualmente existem duplicatas funcionais em `intelligence/` e `legacy/`.
2.  **Centralização de Scrapers:** Consolidar `shadow_market_oracle.py`, `shadow_crawler.py` e `zenith_automation.py` sob um orquestrador de busca (`HarvestManager`).
3.  **Limpeza de Legado:** O diretório `legacy/` contém arquivos que já foram migrados para o core. Recomenda-se mover o `supra_codex.json` para `/config` e arquivar o restante.

### Plano de Expansão v4.1.0+
1.  **Deep-Mind Archive:** Implementar busca vetorial (RAG) nativa na `Ancestral Memory` usando modelos locais (Ollama/vLLM) para reduzir latência de decisão.
2.  **Multi-Cloud Deploy:** Expandir o `Glitch Deploy` para suportar provedores serverless como fallback automático.
3.  **Adversarial Defense:** Treinar o `QA Engine` para realizar ataques simulados (Red Teaming) contra o próprio `The Forge` para garantir código seguro.
