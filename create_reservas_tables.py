#!/usr/bin/env python3
"""
Script para criar as tabelas de clientes e reservas no banco de dados
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = 'backend/database/padaria.db'

def create_reservas_tables():
    """Criar tabelas de clientes e reservas"""
    print("🔧 Criando tabelas de reservas...")
    
    # Verificar se o banco existe
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados não encontrado em: {DB_PATH}")
        print("Execute primeiro o script de criação do banco principal")
        return False
    
    # Criar backup
    backup_path = DB_PATH + '.backup_reservas'
    if os.path.exists(DB_PATH):
        import shutil
        shutil.copy2(DB_PATH, backup_path)
        print(f"✅ Backup criado: {backup_path}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Criar tabela de clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR NOT NULL,
                telefone VARCHAR UNIQUE NOT NULL,
                endereco TEXT NOT NULL,
                data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Tabela 'clientes' criada/verificada")
        
        # Criar tabela de reservas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mesa_id INTEGER NOT NULL,
                cliente_id INTEGER NOT NULL,
                data_reserva DATE NOT NULL,
                horario_reserva VARCHAR NOT NULL,
                status VARCHAR DEFAULT 'ativa',
                observacoes TEXT,
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (mesa_id) REFERENCES mesas (id),
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        """)
        print("✅ Tabela 'reservas' criada/verificada")
        
        # Criar índices para melhor performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_clientes_telefone ON clientes(telefone)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reservas_mesa_data ON reservas(mesa_id, data_reserva)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_reservas_status ON reservas(status)")
        print("✅ Índices criados/verificados")
        
        # Verificar se a coluna status existe na tabela mesas
        cursor.execute("PRAGMA table_info(mesas)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'status' not in columns:
            print("❌ Coluna 'status' não encontrada na tabela 'mesas'")
            print("Adicionando coluna 'status'...")
            cursor.execute("ALTER TABLE mesas ADD COLUMN status VARCHAR DEFAULT 'livre'")
            print("✅ Coluna 'status' adicionada à tabela 'mesas'")
        
        # Verificar se a coluna qr_code existe na tabela mesas
        if 'qr_code' not in columns:
            print("❌ Coluna 'qr_code' não encontrada na tabela 'mesas'")
            print("Adicionando coluna 'qr_code'...")
            cursor.execute("ALTER TABLE mesas ADD COLUMN qr_code VARCHAR")
            print("✅ Coluna 'qr_code' adicionada à tabela 'mesas'")
        
        # Inserir dados de exemplo (opcional)
        print("\n📝 Inserindo dados de exemplo...")
        
        # Inserir clientes de exemplo
        clientes_exemplo = [
            ('João Silva', '(11) 99999-1111', 'Rua das Flores, 123 - Centro'),
            ('Maria Santos', '(11) 99999-2222', 'Av. Principal, 456 - Jardins'),
            ('Pedro Costa', '(11) 99999-3333', 'Rua do Comércio, 789 - Vila Nova')
        ]
        
        for nome, telefone, endereco in clientes_exemplo:
            try:
                cursor.execute("""
                    INSERT INTO clientes (nome, telefone, endereco)
                    VALUES (?, ?, ?)
                """, (nome, telefone, endereco))
                print(f"✅ Cliente '{nome}' inserido")
            except sqlite3.IntegrityError:
                print(f"ℹ️ Cliente '{nome}' já existe")
        
        # Verificar mesas existentes
        cursor.execute("SELECT id, numero FROM mesas")
        mesas = cursor.fetchall()
        
        if mesas:
            print(f"📋 Encontradas {len(mesas)} mesa(s)")
            
            # Inserir algumas reservas de exemplo
            from datetime import datetime, timedelta
            
            # Data de amanhã
            amanha = datetime.now() + timedelta(days=1)
            data_reserva = amanha.strftime('%Y-%m-%d')
            
            # Reservar mesa 1 para João Silva
            try:
                cursor.execute("""
                    INSERT INTO reservas (mesa_id, cliente_id, data_reserva, horario_reserva, observacoes)
                    VALUES (?, ?, ?, ?, ?)
                """, (1, 1, data_reserva, '19:00', 'Aniversário'))
                print(f"✅ Reserva criada para Mesa 1 em {data_reserva} às 19:00")
                
                # Atualizar status da mesa para reservada
                cursor.execute("UPDATE mesas SET status = 'reservada' WHERE id = 1")
                print("✅ Status da Mesa 1 atualizado para 'reservada'")
                
            except sqlite3.IntegrityError as e:
                print(f"ℹ️ Reserva já existe ou erro: {e}")
        
        conn.commit()
        print("\n🎉 Tabelas de reservas criadas com sucesso!")
        
        # Mostrar estrutura final
        print("\n📊 Estrutura final do banco:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = cursor.fetchall()
        
        for tabela in tabelas:
            nome_tabela = tabela[0]
            cursor.execute(f"PRAGMA table_info({nome_tabela})")
            colunas = cursor.fetchall()
            print(f"\n📋 Tabela: {nome_tabela}")
            for col in colunas:
                print(f"   - {col[1]} ({col[2]})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    create_reservas_tables() 