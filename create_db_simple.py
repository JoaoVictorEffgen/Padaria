#!/usr/bin/env python3
"""
Script simples para criar o banco SQLite com todas as tabelas
"""
import sqlite3
import os

def create_database():
    print("🍞 Criando banco de dados SQLite...")
    print("=" * 50)
    
    # Caminho do banco
    db_path = "backend/database/padaria.db"
    
    try:
        # Conectar ao banco (cria se não existir)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("📝 Criando tabelas...")
        
        # Criar tabela produtos com campo estoque
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                categoria TEXT NOT NULL,
                descricao TEXT,
                disponivel BOOLEAN DEFAULT 1,
                estoque INTEGER DEFAULT 0
            )
        """)
        
        # Criar tabela mesas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER UNIQUE NOT NULL,
                status TEXT DEFAULT 'livre',
                qr_code TEXT
            )
        """)
        
        # Criar tabela comandas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comandas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mesa_id INTEGER NOT NULL,
                status TEXT DEFAULT 'aberta',
                total REAL DEFAULT 0.0,
                data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_fechamento DATETIME,
                data_impressao DATETIME,
                observacoes TEXT,
                FOREIGN KEY (mesa_id) REFERENCES mesas (id)
            )
        """)
        
        # Criar tabela itens_comanda
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_comanda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comanda_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER DEFAULT 1,
                preco_unitario REAL NOT NULL,
                observacoes TEXT,
                status TEXT DEFAULT 'pendente',
                FOREIGN KEY (comanda_id) REFERENCES comandas (id),
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        """)
        
        # Criar tabela pedidos_online
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos_online (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_cliente TEXT NOT NULL,
                telefone TEXT NOT NULL,
                endereco TEXT NOT NULL,
                forma_pagamento TEXT NOT NULL,
                total REAL NOT NULL,
                status TEXT DEFAULT 'pendente',
                observacoes TEXT,
                data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_confirmacao DATETIME,
                data_entrega DATETIME,
                whatsapp_enviado BOOLEAN DEFAULT 0
            )
        """)
        
        # Criar tabela itens_pedido_online
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_pedido_online (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER DEFAULT 1,
                preco_unitario REAL NOT NULL,
                observacoes TEXT,
                FOREIGN KEY (pedido_id) REFERENCES pedidos_online (id),
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        """)
        
        conn.commit()
        print("✅ Tabelas criadas com sucesso!")
        
        # Inserir produtos de exemplo
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
        
        # Inserir algumas mesas
        for i in range(1, 6):
            cursor.execute("INSERT INTO mesas (numero, status) VALUES (?, ?)", (i, "livre"))
        
        conn.commit()
        print(f"✅ {len(produtos_exemplo)} produtos e 5 mesas inseridos!")
        
        # Verificar estrutura
        cursor.execute("PRAGMA table_info(produtos)")
        columns = cursor.fetchall()
        print(f"\n📋 Estrutura da tabela produtos:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - Default: {col[4]}")
        
        # Mostrar produtos
        cursor.execute("SELECT id, nome, preco, estoque FROM produtos")
        produtos = cursor.fetchall()
        print(f"\n📦 Produtos no banco:")
        for produto in produtos:
            print(f"  - ID {produto[0]}: {produto[1]} - R$ {produto[2]:.2f} - Estoque: {produto[3]}")
        
        conn.close()
        print("\n🎉 Banco de dados criado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
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