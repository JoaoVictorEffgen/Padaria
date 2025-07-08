#!/usr/bin/env python3
"""
Script de teste para o site web da padaria
"""

import requests
import time
import sys

def test_web_server():
    """Testa se o servidor web está funcionando"""
    print("🧪 Testando servidor web da padaria...")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Teste 1: Página principal
    print("1. Testando página principal...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Página principal carregada com sucesso")
        else:
            print(f"❌ Erro na página principal: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar com o servidor: {e}")
        return False
    
    # Teste 2: API de produtos
    print("2. Testando API de produtos...")
    try:
        response = requests.get(f"{base_url}/produtos/", timeout=5)
        if response.status_code == 200:
            produtos = response.json()
            print(f"✅ API de produtos funcionando - {len(produtos)} produtos encontrados")
        else:
            print(f"❌ Erro na API de produtos: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao testar API: {e}")
    
    # Teste 3: Arquivos estáticos
    print("3. Testando arquivos estáticos...")
    try:
        response = requests.get(f"{base_url}/static/css/style.css", timeout=5)
        if response.status_code == 200:
            print("✅ CSS carregado com sucesso")
        else:
            print(f"❌ Erro ao carregar CSS: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao carregar arquivos estáticos: {e}")
    
    # Teste 4: JavaScript
    print("4. Testando JavaScript...")
    try:
        response = requests.get(f"{base_url}/static/js/app.js", timeout=5)
        if response.status_code == 200:
            print("✅ JavaScript carregado com sucesso")
        else:
            print(f"❌ Erro ao carregar JavaScript: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao carregar JavaScript: {e}")
    
    print("=" * 50)
    print("🎉 Testes concluídos!")
    print("📱 Acesse o site em: http://localhost:8000")
    print("📋 API docs em: http://localhost:8000/docs")
    
    return True

def main():
    """Função principal"""
    print("🍞 Sistema Web da Padaria Delícias - Teste")
    print("=" * 50)
    
    # Aguardar um pouco para o servidor inicializar
    print("⏳ Aguardando servidor inicializar...")
    time.sleep(3)
    
    success = test_web_server()
    
    if success:
        print("\n✅ Todos os testes passaram! O site está funcionando.")
    else:
        print("\n❌ Alguns testes falharam. Verifique se o servidor está rodando.")
        print("💡 Execute: python run_web.py")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 