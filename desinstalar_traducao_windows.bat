@echo off
setlocal
chcp 65001 >nul
title Desinstalador Traducao PT-BR - Unicorn Overlord
echo =====================================================================
echo              DESINSTALAR TRADUCAO PT-BR - UNICORN OVERLORD
echo                  (Devolve os arquivos originais do jogo)
echo =====================================================================
echo.

set "PY="
py -3 --version >nul 2>nul && set "PY=py -3"
if not defined PY python --version >nul 2>nul && set "PY=python"
if not defined PY (
    echo [ERRO] Python 3 nao encontrado no sistema.
    pause
    exit /b 1
)

set "TARGET=%~1"
%PY% "%~dp0ferramentas\patcher.py" revert "%TARGET%"
set "RESULT=%errorlevel%"

echo.
pause
exit /b %RESULT%
