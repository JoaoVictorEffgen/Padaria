@echo off
echo ========================================
echo    INSTALADOR DE PYTHON - WINDOWS
echo ========================================
echo.
echo Este script vai ajudar você a instalar o Python
echo necessário para o Sistema de Padaria.
echo.

echo Verificando se Python ja esta instalado...
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Python ja esta instalado!
    python --version
    echo.
    echo Execute: python start_system.py
    pause
    exit /b 0
)

echo ❌ Python nao encontrado.
echo.
echo Opcoes de instalacao:
echo.
echo 1. Microsoft Store (Recomendado)
echo    - Abra Microsoft Store
echo    - Procure por "Python"
echo    - Instale a versao mais recente
echo.
echo 2. Download direto
echo    - Acesse: https://www.python.org/downloads/
echo    - Baixe a versao mais recente
echo    - IMPORTANTE: Marque "Add Python to PATH"
echo.
echo 3. Instalacao automatica (experimental)
echo    - Este script tentara baixar e instalar automaticamente
echo.

set /p choice="Escolha uma opcao (1, 2 ou 3): "

if "%choice%"=="1" (
    echo.
    echo Abrindo Microsoft Store...
    start ms-windows-store://pdp/?ProductId=9NRWMJP3717K
    echo.
    echo Apos instalar, execute: python start_system.py
    pause
    exit /b 0
)

if "%choice%"=="2" (
    echo.
    echo Abrindo pagina de download do Python...
    start https://www.python.org/downloads/
    echo.
    echo Apos instalar, execute: python start_system.py
    pause
    exit /b 0
)

if "%choice%"=="3" (
    echo.
    echo Tentando instalacao automatica...
    echo Baixando Python...
    
    REM Tentar baixar Python usando winget
    winget install Python.Python.3.11 >nul 2>&1
    if %errorlevel% == 0 (
        echo ✅ Python instalado com sucesso via winget!
        echo.
        echo Execute: python start_system.py
        pause
        exit /b 0
    )
    
    echo ❌ Falha na instalacao automatica.
    echo Tente as opcoes 1 ou 2.
    pause
    exit /b 1
)

echo Opcao invalida.
pause
exit /b 1 