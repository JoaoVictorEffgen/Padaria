#!/usr/bin/env python3
"""
Script para iniciar o servidor web da padaria
"""

import uvicorn
import os
import sys

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def main():
    """Inicia o servidor web"""
    print("🍞 Iniciando Sistema Web da Padaria Delícias...")
    print("=" * 50)
    
    
    host = "0.0.0.0"
    port = 8001
    reload = True
    
    print(f"📍 Servidor rodando em: http://localhost:{port}")
    print(f"🌐 Acesso externo: http://0.0.0.0:{port}")
    print("=" * 50)
    print("📱 Site da padaria disponível em: http://localhost:8000")
    print("📋 API disponível em: http://localhost:8000/docs")
    print("=" * 50)
    print("🛑 Para parar o servidor, pressione Ctrl+C")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 