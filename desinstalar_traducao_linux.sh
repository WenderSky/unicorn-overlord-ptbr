#!/usr/bin/env bash
# Desinstalador da Tradução PT-BR de Unicorn Overlord para Steam Deck / Linux
# Uso: ./desinstalar_traducao_linux.sh [pasta do jogo]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "====================================================================="
echo "            DESINSTALAR TRADUCAO PT-BR - UNICORN OVERLORD"
echo "====================================================================="
echo

if ! command -v python3 &>/dev/null; then
    echo "Erro: Python 3 nao encontrado."
    exit 1
fi

python3 "$SCRIPT_DIR/ferramentas/patcher.py" revert "${1:-}"
exit $?
