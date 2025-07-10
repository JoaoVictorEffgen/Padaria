#!/usr/bin/env python3
"""
Script para inicializar o banco de dados e adicionar o campo 'estoque'
"""
import os
import sys
import sqlite3

# Adicionar o backend ao path
sys.path.append('backend')

from backend.app.database import engine
from backend.app.models import Base

def init_database():
    print("🍞 Inicializando banco de dados da padaria...")
    print("=" * 50)
    
    try:
        # Criar todas as tabelas
        print("📝 Criando tabelas...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        
        # Verificar se o campo estoque existe
        db_path = "backend/database/padaria.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estrutura da tabela produtos
        cursor.execute("PRAGMA table_info(produtos)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'estoque' not in column_names:
            print("📝 Adicionando campo 'estoque' na tabela produtos...")
            cursor.execute("ALTER TABLE produtos ADD COLUMN estoque INTEGER DEFAULT 0")
            
            # Atualizar produtos existentes com estoque padrão
            cursor.execute("UPDATE produtos SET estoque = 10 WHERE estoque IS NULL")
            conn.commit()
            print("✅ Campo 'estoque' adicionado com sucesso!")
        else:
            print("✅ Campo 'estoque' já existe!")
        
        # Mostrar estrutura final
        cursor.execute("PRAGMA table_info(produtos)")
        columns = cursor.fetchall()
        print("\n📋 Estrutura da tabela produtos:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - Default: {col[4]}")
        
        # Inserir alguns produtos de exemplo se a tabela estiver vazia
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
        print(f"\n📦 Produtos no banco (mostrando até 10):")
        for produto in produtos:
            print(f"  - ID {produto[0]}: {produto[1]} - R$ {produto[2]:.2f} - Estoque: {produto[3]}")
        
        conn.close()
        print("\n🎉 Banco de dados inicializado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    
    if success:
        print("\n💡 Agora você pode:")
        print("  1. Iniciar o backend: python run_backend.py")
        print("  2. Iniciar o desktop: python run_desktop.py")
        print("  3. Iniciar o web: python run_web.py")
    else:
        print("\n❌ Falha na inicialização. Verifique os erros acima.") 