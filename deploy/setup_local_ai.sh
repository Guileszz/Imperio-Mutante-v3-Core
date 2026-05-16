#!/bin/bash
# setup_local_ai.sh - Script de instalação do ecossistema de IA Bare-Metal para Império Mutante v4

set -e

echo "🚀 [CAMINHO 1] Iniciando Setup de IA Local (Cérebro Local)..."

# 1. Instalar Ollama
if ! command -v ollama &> /dev/null
then
    echo "📦 Instalando Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "✅ Ollama já está instalado."
fi

# 2. Configurar variáveis de ambiente otimizadas para o Ryzen 9
# Adiciona ao .bashrc para persistência se necessário, ou apenas exporta agora
export OLLAMA_NUM_PARALLEL=4
export OMP_NUM_THREADS=32
echo "⚙️ Hardware otimizado: 32 threads Ryzen 9 mapeadas para Ollama."

# 3. Download de modelos otimizados
echo "📥 Baixando modelos (Llama 3 e DeepSeek-Coder)..."
ollama pull llama3
ollama pull deepseek-coder:6.7b

# 4. Pre-load dos modelos para minimizar latência inicial
echo "🧠 Realizando pre-load do Llama 3..."
curl -s -X POST http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "",
  "keep_alive": -1
}' > /dev/null

echo "✅ [CAMINHO 1] IA Local (NEURO-TOXINA) pronta para combate!"
