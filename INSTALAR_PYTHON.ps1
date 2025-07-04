# Script PowerShell para instalar Python
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    INSTALADOR DE PYTHON - WINDOWS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Este script vai ajudar você a instalar o Python" -ForegroundColor Yellow
Write-Host "necessário para o Sistema de Padaria." -ForegroundColor Yellow
Write-Host ""

# Verificar se Python já está instalado
Write-Host "Verificando se Python já está instalado..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python já está instalado!" -ForegroundColor Green
        Write-Host $pythonVersion -ForegroundColor White
        Write-Host ""
        Write-Host "Execute: python start_system.py" -ForegroundColor Yellow
        Read-Host "Pressione Enter para continuar"
        exit 0
    }
} catch {
    # Python não encontrado
}

Write-Host "❌ Python não encontrado." -ForegroundColor Red
Write-Host ""
Write-Host "Opções de instalação:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Microsoft Store (Recomendado)" -ForegroundColor Cyan
Write-Host "   - Abra Microsoft Store" -ForegroundColor White
Write-Host "   - Procure por 'Python'" -ForegroundColor White
Write-Host "   - Instale a versão mais recente" -ForegroundColor White
Write-Host ""
Write-Host "2. Download direto" -ForegroundColor Cyan
Write-Host "   - Acesse: https://www.python.org/downloads/" -ForegroundColor White
Write-Host "   - Baixe a versão mais recente" -ForegroundColor White
Write-Host "   - IMPORTANTE: Marque 'Add Python to PATH'" -ForegroundColor White
Write-Host ""
Write-Host "3. Instalação automática (experimental)" -ForegroundColor Cyan
Write-Host "   - Este script tentará baixar e instalar automaticamente" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Escolha uma opção (1, 2 ou 3)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Abrindo Microsoft Store..." -ForegroundColor Green
        Start-Process "ms-windows-store://pdp/?ProductId=9NRWMJP3717K"
        Write-Host ""
        Write-Host "Após instalar, execute: python start_system.py" -ForegroundColor Yellow
        Read-Host "Pressione Enter para continuar"
        exit 0
    }
    "2" {
        Write-Host ""
        Write-Host "Abrindo página de download do Python..." -ForegroundColor Green
        Start-Process "https://www.python.org/downloads/"
        Write-Host ""
        Write-Host "Após instalar, execute: python start_system.py" -ForegroundColor Yellow
        Read-Host "Pressione Enter para continuar"
        exit 0
    }
    "3" {
        Write-Host ""
        Write-Host "Tentando instalação automática..." -ForegroundColor Green
        Write-Host "Baixando Python..." -ForegroundColor Yellow
        
        # Tentar usar winget
        try {
            Write-Host "Tentando instalar via winget..." -ForegroundColor Yellow
            winget install Python.Python.3.11
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Python instalado com sucesso via winget!" -ForegroundColor Green
                Write-Host ""
                Write-Host "Execute: python start_system.py" -ForegroundColor Yellow
                Read-Host "Pressione Enter para continuar"
                exit 0
            }
        } catch {
            Write-Host "winget não disponível, tentando Chocolatey..." -ForegroundColor Yellow
        }
        
        # Tentar usar Chocolatey
        try {
            Write-Host "Tentando instalar via Chocolatey..." -ForegroundColor Yellow
            choco install python -y
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Python instalado com sucesso via Chocolatey!" -ForegroundColor Green
                Write-Host ""
                Write-Host "Execute: python start_system.py" -ForegroundColor Yellow
                Read-Host "Pressione Enter para continuar"
                exit 0
            }
        } catch {
            Write-Host "Chocolatey não disponível." -ForegroundColor Red
        }
        
        Write-Host "❌ Falha na instalação automática." -ForegroundColor Red
        Write-Host "Tente as opções 1 ou 2." -ForegroundColor Yellow
        Read-Host "Pressione Enter para continuar"
        exit 1
    }
    default {
        Write-Host "Opção inválida." -ForegroundColor Red
        Read-Host "Pressione Enter para continuar"
        exit 1
    }
} 