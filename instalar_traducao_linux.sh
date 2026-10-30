#!/usr/bin/env bash
# Instalador da Tradução PT-BR de Unicorn Overlord para Steam Deck / Linux
# Uso: ./instalar_traducao_linux.sh [pasta do jogo]
# Sem argumento, o patcher procura o jogo sozinho e, se nao achar, pergunta.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "====================================================================="
echo "        TRADUCAO PORTUGUES BRASILEIRO (PT-BR) - UNICORN OVERLORD"
echo "                         (Steam Deck / Linux)"
echo "====================================================================="
echo

if ! command -v python3 &>/dev/null; then
    echo "Erro: Python 3 nao encontrado."
    exit 1
fi

python3 "$SCRIPT_DIR/ferramentas/patcher.py" apply "${1:-}" "$SCRIPT_DIR/arquivos_traducao"
status=$?
echo
if [ $status -eq 0 ]; then
    echo "[SUCESSO] Traducao PT-BR instalada! Deixe o Text Language do jogo em auto."
else
    echo "[ERRO] A traducao nao foi instalada. Veja a mensagem acima."
fi
exit $status
