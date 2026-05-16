# 📖 MANUAL OPERACIONAL v3.5.0: CLUSTER SOBERANO

Este guia descreve a operação do cluster multi-nó do Império Mutante, incluindo os novos sistemas de precisão temporal e memória de longo prazo.

---

## 🏛️ Arquitetura do Cluster

O sistema opera em uma tríade de nós especializados:

1.  **🔵 SPECTRUM (Eficiência)**
    *   **Hardware**: Linux / RTX 3050.
    *   **Função**: Host de Telemetria, Zenith Automation, Alquimia (Porta 8001).
2.  **🔴 NEURO-TOXIN (Poder)**
    *   **Hardware**: Ryzen 9 (32 Threads) / RTX 3070.
    *   **Função**: Processamento Neural Pesado, Shadow Oracle, Chronos Engine.
3.  **🟡 GLITCH (Resiliência)**
    *   **Hardware**: Edge / Mobile / Fallback.
    *   **Função**: Deploy de ativos, interface C2 de emergência.

---

## 🛠️ Configuração Inicial

### 1. Requisitos de Ambiente
*   Python 3.10+
*   Redis (para Knowledge Store da Alquimia)
*   ChromaDB (para Memória Ancestral)
*   Chaves de API: Gemini 1.5 Flash (essencial).

### 2. Variáveis de Ambiente (.env)
```env
GEMINI_API_KEY=sua_chave
GITHUB_TOKEN=seu_token
TELEGRAM_TOKEN=seu_bot_token
TELEGRAM_CHAT_ID=seu_chat_id
CHRONOS_WORKERS=32
```

---

## 🌀 Novos Sistemas v3.5.0

### 🕰️ CHRONOS: O Guardião do Tempo
O Chronos utiliza o poder do Ryzen 9 para executar centenas de simulações de Monte Carlo em paralelo.
*   **Como usar**: O Nexus Core dispara o Chronos automaticamente ao detectar anomalias de preço via Shadow Oracle.
*   **Saída**: Score de viabilidade (0.0 a 1.0) e classificação de risco.

### 🧠 Memória Ancestral (RAG)
Sistema de memória vetorial que impede que o Império esqueça lições aprendidas.
*   **Indexação**: Toda extração do `/HARVEST` bem-sucedida é automaticamente ancorada na Memória Ancestral.
*   **Recuperação**: O Nexus Core consulta a memória antes de tomar decisões críticas ou responder a comandos `/SOBERANIA`.

---

## 🚀 Fluxo de Trabalho Recomendado

1.  **Ignição**: Execute `./ignite_empire.sh` para subir todos os serviços.
2.  **Monitoramento**: Utilize o comando `/SOBERANIA` no Telegram para verificar a saúde dos nós.
3.  **Alimentação**: Agende `/HARVEST` periódicos para manter o fluxo de Néctar.
4.  **Expansão**: Use `/FORJAR` para criar novos Micro-SaaS baseados nas tendências detectadas pelo Shadow Oracle.

---

## 🛡️ Protocolos de Defesa
*   O **CARRASCO** monitora o uso de recursos a cada 60 segundos.
*   Se um processo não-identificado consumir > 15% de CPU, ele é eliminado sumariamente para garantir a soberania do Nexus Core.

---
*Soberania através da Automação.*
