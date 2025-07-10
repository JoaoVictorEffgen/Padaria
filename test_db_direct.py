#!/usr/bin/env python3
"""
Teste direto do banco SQLite
"""
import sqlite3

def test_database():
    print("🔍 Testando banco de dados diretamente...")
    print("=" * 50)
    
    try:
        # Conectar ao banco
        conn = sqlite3.connect('backend/database/padaria.db')
        cursor = conn.cursor()
        
        # Verificar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tabelas encontradas: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Verificar produtos
        cursor.execute("SELECT COUNT(*) FROM produtos")
        count = cursor.fetchone()[0]
        print(f"\n📦 Total de produtos: {count}")
        
        # Mostrar produtos com estoque
        cursor.execute("SELECT id, nome, preco, estoque, disponivel FROM produtos")
        produtos = cursor.fetchall()
        print(f"\n📦 Produtos com estoque:")
        for produto in produtos:
            print(f"  - ID {produto[0]}: {produto[1]} - R$ {produto[2]:.2f} - Estoque: {produto[3]} - Disponível: {produto[4]}")
        
        # Verificar estrutura da tabela produtos
        cursor.execute("PRAGMA table_info(produtos)")
        columns = cursor.fetchall()
        print(f"\n📋 Estrutura da tabela produtos:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - Default: {col[4]}")
        
        conn.close()
        print("\n✅ Banco de dados funcionando corretamente!")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    test_database() 