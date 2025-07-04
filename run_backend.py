#!/usr/bin/env python3
"""
Script para executar o backend da API
"""
import os
import sys
import subprocess

def main():
    # Verificar se estamos no diretório correto
    if not os.path.exists("backend/app/main.py"):
        print("Erro: Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    # Instalar dependências se necessário
    # print("Verificando dependências...")
    # try:
    #     subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
    #                   check=True, capture_output=True)
    #     print("Dependências instaladas com sucesso!")
    # except subprocess.CalledProcessError:
    #     print("Erro ao instalar dependências")
    #     sys.exit(1)
    
    # Executar o backend
    print("Iniciando backend...")
    print("API estará disponível em: http://localhost:8000")
    print("Documentação: http://localhost:8000/docs")
    print("Pressione Ctrl+C para parar")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "backend.app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\nBackend parado.")

if __name__ == "__main__":
    main() 