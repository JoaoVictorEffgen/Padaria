#!/usr/bin/env python3
"""
Script para executar o sistema desktop
"""
import os
import sys
import subprocess

def main():
    # Verificar se estamos no diretório correto
    if not os.path.exists("desktop/main.py"):
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
    
    # Executar o sistema desktop
    print("Iniciando sistema desktop...")
    print("Certifique-se de que o backend está rodando em http://localhost:8000")
    
    try:
        # Adicionar o diretório desktop ao path
        sys.path.insert(0, os.path.join(os.getcwd(), "desktop"))
        
        # Executar o sistema desktop
        subprocess.run([sys.executable, "desktop/main.py"])
    except KeyboardInterrupt:
        print("\nSistema desktop parado.")
    except Exception as e:
        print(f"Erro ao executar sistema desktop: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 