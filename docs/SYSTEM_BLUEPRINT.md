# 🗺️ SYSTEM BLUEPRINT: IMPÉRIO MUTANTE v4.0.0 Alpha

Este documento mapeia a topologia técnica e as interações entre os núcleos do ecossistema, agora com foco na **IA Híbrida**.

---

## 📂 Mapeamento de Diretórios

```text
/home/engine/project
├── core/                   # Cérebro Central e Orquestração
│   ├── nexus_core.py       # Orquestrador Central (FastAPI)
│   ├── local_brain_bridge.py # Ponte de IA Híbrida (Cloud vs Local)
│   ├── telemetry.py        # Coleta de métricas GPU/CPU
│   └── evolution_engine.py # Motor de auto-otimização
├── intelligence/           # Núcleos de Inteligência e Dados
│   ├── ancestral_memory.py # Vetor store (RAG) / ChromaDB
│   ├── chronos.py          # Motor de predição Monte Carlo
│   ├── zenith_automation.py # Extração recursiva de Néctar
│   └── ...
├── defense/                # Camadas de Proteção e Qualidade
├── interface/              # Cockpit e Controle (C2)
├── deploy/                 # Automação de Infraestrutura
│   ├── setup_local_ai.sh   # Instalador do ecossistema IA Local
│   └── the_bridge.py       # Pipeline CI/CD autônomo
├── legacy/                 # Base de Dados e Supra-Codex
└── docs/                   # Documentação de Soberania
```

---

## 🔄 Fluxo de Dados: Ciclo da IA Híbrida

1.  **Ingresso**: Dados brutos entram via `/ingress` ou chamadas internas.
2.  **Roteamento (Local Brain Bridge)**:
    - O sistema tenta processar via **Gemini 1.5 Flash (Cloud)**.
    - Se o tempo de resposta exceder **3 segundos** ou houver falha de rede, o fallback é acionado.
3.  **Processamento Local**: A carga é desviada para o nó **NEURO-TOXINA** (Ollama) utilizando os 32 núcleos do Ryzen 9 e a RTX 3070.
4.  **Ação**: O resultado é processado pelo Nexus Core para execução de comandos ou forja de ativos.

---

## 🏛️ Interações entre Núcleos

*   **Nexus ↔ Local Brain Bridge**: O Nexus delega toda a classificação e síntese para a bridge, garantindo resiliência.
*   **Bridge ↔ Ollama**: Interface com modelos Llama 3 e DeepSeek rodando bare-metal.
*   **Chronos ↔ Ryzen 9**: Simulações massivas paralelas para predição financeira.

---

## 📡 Portos e Serviços

| Serviço | Porto | Nó |
| :--- | :--- | :--- |
| Nexus Core | 8000 | Central |
| Ollama API | 11434 | NEURO-TOXIN |
| Alquimia | 8001 | SPECTRUM |
| Neuro-Toxin | 8002 | NEURO-TOXIN |
| Glitch | 8003 | GLITCH |

---
*Blueprint atualizado para a versão 4.0.0 Alpha - Caminho 1: Cérebro Local.*
