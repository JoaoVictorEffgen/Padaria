#!/usr/bin/env python3
"""
Script para testar a finalização automática de comandas
Simula o processo de finalização no desktop e verifica se o mobile detecta
"""

import requests
import time
import json
from datetime import datetime

# Configuração
API_BASE_URL = "http://localhost:8000"

def listar_comandas():
    """Lista todas as comandas"""
    try:
        response = requests.get(f"{API_BASE_URL}/comandas/")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao listar comandas: {response.status_code}")
            return []
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return []

def obter_comanda(comanda_id):
    """Obtém detalhes de uma comanda específica"""
    try:
        response = requests.get(f"{API_BASE_URL}/comandas/{comanda_id}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao obter comanda {comanda_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return None

def finalizar_comanda(comanda_id):
    """Finaliza uma comanda (simula o desktop)"""
    try:
        response = requests.put(f"{API_BASE_URL}/comandas/{comanda_id}/finalizar")
        if response.status_code == 200:
            print(f"✅ Comanda {comanda_id} finalizada com sucesso!")
            return True
        else:
            print(f"❌ Erro ao finalizar comanda {comanda_id}: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def monitorar_comanda(comanda_id, duracao=30):
    """Monitora uma comanda por um período"""
    print(f"\n🔍 Monitorando comanda {comanda_id} por {duracao} segundos...")
    print("=" * 50)
    
    inicio = time.time()
    while time.time() - inicio < duracao:
        comanda = obter_comanda(comanda_id)
        if comanda:
            status = comanda.get('status', 'desconhecido')
            total = comanda.get('total', 0)
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Comanda {comanda_id}: Status={status}, Total=R${total:.2f}")
            
            if status == "fechada":
                print("🎉 Comanda foi finalizada!")
                break
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Erro ao obter comanda")
        
        time.sleep(2)  # Verificar a cada 2 segundos

def main():
    print("🍞 Teste de Finalização Automática de Comandas")
    print("=" * 50)
    
    # 1. Listar comandas existentes
    print("\n1️⃣ Listando comandas existentes...")
    comandas = listar_comandas()
    
    if not comandas:
        print("❌ Nenhuma comanda encontrada. Abra uma comanda no mobile primeiro.")
        return
    
    print(f"📋 Encontradas {len(comandas)} comanda(s):")
    for comanda in comandas:
        status = comanda.get('status', 'desconhecido')
        total = comanda.get('total', 0)
        mesa = comanda.get('mesa_numero', 'N/A')
        print(f"   - Comanda {comanda['id']} (Mesa {mesa}): Status={status}, Total=R${total:.2f}")
    
    # 2. Encontrar comanda aberta para testar
    comanda_aberta = None
    for comanda in comandas:
        if comanda.get('status') == 'aberta':
            comanda_aberta = comanda
            break
    
    if not comanda_aberta:
        print("\n❌ Nenhuma comanda aberta encontrada. Abra uma comanda no mobile primeiro.")
        return
    
    comanda_id = comanda_aberta['id']
    print(f"\n✅ Comanda {comanda_id} selecionada para teste")
    
    # 3. Instruções para o usuário
    print("\n📱 INSTRUÇÕES PARA O TESTE:")
    print("1. Abra o app mobile/tablet")
    print("2. Abra uma comanda (se não tiver uma aberta)")
    print("3. Observe que aparece 'Monitorando...' no cabeçalho")
    print("4. Execute este script para finalizar a comanda")
    print("5. Observe que o mobile detecta automaticamente e mostra 'Comanda Finalizada!'")
    
    input("\n⏳ Pressione ENTER quando estiver pronto para finalizar a comanda...")
    
    # 4. Finalizar comanda
    print(f"\n🚀 Finalizando comanda {comanda_id}...")
    if finalizar_comanda(comanda_id):
        print("\n✅ Comanda finalizada! Verifique o mobile em 5-10 segundos.")
        print("📱 O mobile deve mostrar automaticamente a tela de 'Comanda Finalizada!'")
    else:
        print("\n❌ Falha ao finalizar comanda")
    
    # 5. Monitorar por alguns segundos
    print("\n⏱️ Monitorando por mais alguns segundos...")
    monitorar_comanda(comanda_id, 10)
    
    print("\n🎯 Teste concluído!")
    print("📱 Verifique se o mobile detectou a finalização automaticamente")

if __name__ == "__main__":
    main() 