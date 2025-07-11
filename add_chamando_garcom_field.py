#!/usr/bin/env python3
"""
Script para adicionar o campo 'chamando_garcom' na tabela comandas
"""
import os
import sys
import sqlite3

def add_chamando_garcom_field():
    print("🍞 Adicionando campo 'chamando_garcom' na tabela comandas...")
    print("=" * 60)
    
    try:
        # Conectar ao banco
        db_path = "backend/database/padaria.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estrutura atual da tabela comandas
        cursor.execute("PRAGMA table_info(comandas)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print("📋 Estrutura atual da tabela comandas:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - Default: {col[4]}")
        
        # Verificar se o campo já existe
        if 'chamando_garcom' not in column_names:
            print("\n📝 Adicionando campo 'chamando_garcom' na tabela comandas...")
            cursor.execute("ALTER TABLE comandas ADD COLUMN chamando_garcom BOOLEAN DEFAULT 0")
            conn.commit()
            print("✅ Campo 'chamando_garcom' adicionado com sucesso!")
        else:
            print("\n✅ Campo 'chamando_garcom' já existe!")
        
        # Mostrar estrutura final
        cursor.execute("PRAGMA table_info(comandas)")
        columns = cursor.fetchall()
        print("\n📋 Estrutura final da tabela comandas:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - Default: {col[4]}")
        
        # Verificar comandas existentes
        cursor.execute("SELECT COUNT(*) FROM comandas")
        count = cursor.fetchone()[0]
        print(f"\n📊 Total de comandas no banco: {count}")
        
        # Mostrar algumas comandas de exemplo
        cursor.execute("SELECT id, mesa_id, status, chamando_garcom FROM comandas LIMIT 5")
        comandas = cursor.fetchall()
        if comandas:
            print("\n📋 Comandas existentes (mostrando até 5):")
            for comanda in comandas:
                print(f"  - ID {comanda[0]}: Mesa {comanda[1]} - Status: {comanda[2]} - Chamando: {comanda[3]}")
        
        conn.close()
        print("\n🎉 Campo 'chamando_garcom' configurado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao adicionar campo: {e}")
        return False

if __name__ == "__main__":
    success = add_chamando_garcom_field()
    
    if success:
        print("\n💡 Próximos passos:")
        print("  1. O backend já deve estar rodando e detectou as mudanças")
        print("  2. Agora vamos ajustar o endpoint de chamar garçom")
        print("  3. Implementar o alerta visual no desktop")
    else:
        print("\n❌ Falha na adição do campo. Verifique os erros acima.") 