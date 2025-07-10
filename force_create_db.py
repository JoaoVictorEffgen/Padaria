#!/usr/bin/env python3
"""
Script para forçar a criação das tabelas
"""
import os
import sys

# Adicionar o backend ao path
sys.path.append('backend')

from backend.app.database import engine
from backend.app.models import Base, Produto, Mesa, Comanda, ItemComanda, Garcom, AtendimentoGarcom, SincronizacaoOffline, PedidoOnline, ItemPedidoOnline

def create_database():
    print("🍞 Forçando criação do banco de dados...")
    print("=" * 50)
    
    try:
        # Remover banco existente se estiver vazio
        db_path = "backend/database/padaria.db"
        if os.path.exists(db_path) and os.path.getsize(db_path) == 0:
            os.remove(db_path)
            print("🗑️ Removido banco vazio")
        
        # Criar todas as tabelas
        print("📝 Criando tabelas...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        
        # Verificar se funcionou
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"\n📋 Tabelas criadas: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Verificar estrutura da tabela produtos
        if ('produtos',) in tables:
            cursor.execute("PRAGMA table_info(produtos)")
            columns = cursor.fetchall()
            print(f"\n📋 Estrutura da tabela produtos:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]}) - Default: {col[4]}")
            
            # Verificar se o campo estoque existe
            column_names = [col[1] for col in columns]
            if 'estoque' not in column_names:
                print("\n📝 Adicionando campo 'estoque'...")
                cursor.execute("ALTER TABLE produtos ADD COLUMN estoque INTEGER DEFAULT 0")
                conn.commit()
                print("✅ Campo 'estoque' adicionado!")
            
            # Inserir produtos de exemplo
            cursor.execute("SELECT COUNT(*) FROM produtos")
            count = cursor.fetchone()[0]
            
            if count == 0:
                print("\n📦 Inserindo produtos de exemplo...")
                produtos_exemplo = [
                    ("Pão Francês", 0.50, "Pães", "Pão francês tradicional", 50),
                    ("Croissant", 3.50, "Pães", "Croissant de manteiga", 30),
                    ("Bolo de Chocolate", 25.00, "Bolos", "Bolo de chocolate caseiro", 5),
                    ("Café Expresso", 2.50, "Bebidas", "Café expresso", 100),
                    ("Suco Natural", 4.00, "Bebidas", "Suco natural de laranja", 20)
                ]
                
                for produto in produtos_exemplo:
                    cursor.execute("""
                        INSERT INTO produtos (nome, preco, categoria, descricao, estoque, disponivel)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, produto + (True,))
                
                conn.commit()
                print(f"✅ {len(produtos_exemplo)} produtos inseridos!")
            
            # Mostrar produtos
            cursor.execute("SELECT id, nome, preco, estoque FROM produtos LIMIT 10")
            produtos = cursor.fetchall()
            print(f"\n📦 Produtos no banco:")
            for produto in produtos:
                print(f"  - ID {produto[0]}: {produto[1]} - R$ {produto[2]:.2f} - Estoque: {produto[3]}")
        
        conn.close()
        print("\n🎉 Banco de dados criado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_database()
    
    if success:
        print("\n💡 Agora você pode:")
        print("  1. Iniciar o backend: python run_backend.py")
        print("  2. Iniciar o desktop: python run_desktop.py")
        print("  3. Iniciar o web: python run_web.py")
    else:
        print("\n❌ Falha na criação. Verifique os erros acima.") 