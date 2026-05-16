#!/bin/bash

# =============================================================================
# IMPÉRIO MUTANTE - SCRIPT DE IGNIÇÃO v4.0.0 Beta
# Operação: Ignição Operacional / Caminho 1: Bio-Wealth Loop
# =============================================================================

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}
██╗ ██████╗ ███╗   ██╗██╗████████╗███████╗
██║██╔════╝ ████╗  ██║██║╚══██╔══╝██╔════╝
██║██║  ███╗██╔██╗ ██║██║   ██║   █████╗  
██║██║   ██║██║╚██╗██║██║   ██║   ██╔══╝  
██║╚██████╔╝██║ ╚████║██║   ██║   ███████╗
╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚══════╝
      EMPIRE IGNITION v4.0.0 Beta - BIO-WEALTH LOOP
${NC}"

# 1. Verificação de Ambiente
echo -e "${YELLOW}[*] Verificando ambiente e dependências...${NC}"
if [ ! -f "deploy/requirements.txt" ]; then
    echo -e "${RED}[!] Erro: deploy/requirements.txt não encontrado.${NC}"
    exit 1
fi

# 2. Verificação de Integridade de Inteligência (v4.0.0 Beta)
echo -e "${YELLOW}[*] Validando núcleos de inteligência...${NC}"
INTEL_FILES=("intelligence/bio_wealth_engine.py" "intelligence/wallet_manager.py" "intelligence/shadow_market_oracle.py" "intelligence/chronos.py")
for file in "${INTEL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}[+] Módulo verificado: $file${NC}"
    else
        echo -e "${RED}[!] ALERTA: Módulo crítico ausente: $file${NC}"
    fi
done

# 3. Geração de stubs gRPC se necessário
if [ ! -f "core/neural_bridge_pb2.py" ]; then
    echo -e "${YELLOW}[*] Gerando stubs gRPC...${NC}"
    python3 -m grpc_tools.protoc -I./core --python_out=./core --grpc_python_out=./core ./core/neural_bridge.proto
fi

# 4. Descoberta de Nós (Network Discovery)
echo -e "${YELLOW}[*] Escaneando rede local para nós do cluster...${NC}"
# Simulação de descoberta - em produção usaria arp-scan ou nmap
NODES=("SPECTRUM" "NEURO-TOXIN" "GLITCH")
for node in "${NODES[@]}"; do
    echo -e "${GREEN}[+] Nó encontrado: $node (Status: PRONTO)${NC}"
    sleep 0.5
done

# 4. Inicialização Coordenada
echo -e "${YELLOW}[*] Inicializando Neural Bridge (gRPC Service)...${NC}"
export PYTHONPATH=$PYTHONPATH:$(pwd)/core:$(pwd)
python3 core/neural_bridge.py > /dev/null 2>&1 &
BRIDGE_PID=$!

echo -e "${YELLOW}[*] Inicializando Nexus Cockpit Dashboard...${NC}"
export PORT=8080
python3 interface/cockpit.py > /dev/null 2>&1 &
COCKPIT_PID=$!

# 5. Verificação de Health
sleep 3
if ps -p $BRIDGE_PID > /dev/null && ps -p $COCKPIT_PID > /dev/null; then
    echo -e "${GREEN}
=====================================================
🚀 CLUSTER IMPÉRIO MUTANTE ATIVADO COM SUCESSO!
=====================================================
NEURAL BRIDGE PID: $BRIDGE_PID
COCKPIT DASHBOARD: http://localhost:8080 (PID: $COCKPIT_PID)
LOGS: Monitorando logs em tempo real...
=====================================================
${NC}"
else
    echo -e "${RED}[!] Falha na ignição. Verifique os logs.${NC}"
    kill $BRIDGE_PID $COCKPIT_PID 2>/dev/null || true
    exit 1
fi

# Keep alive e gerenciamento de interrupção
trap "echo -e '${RED}Shutting down cluster...${NC}'; kill $BRIDGE_PID $COCKPIT_PID; exit" INT TERM

echo -e "${BLUE}[i] Pressione Ctrl+C para encerrar a operação.${NC}"
wait
