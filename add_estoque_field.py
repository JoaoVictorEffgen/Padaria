#!/usr/bin/env python3
"""
Script para adicionar o campo 'estoque' na tabela 'produtos'
"""
import sqlite3
import os

def add_estoque_field():
    # Caminho do banco de dados
    db_path = "backend/database/padaria.db"
    
    # Verificar se o banco existe
    if not os.path.exists(db_path):
        print(f"❌ Banco de dados não encontrado em: {db_path}")
        return False
    
    try:
        # Conectar ao banco
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Verificando estrutura atual da tabela produtos...")
        
        # Verificar se o campo estoque já existe
        cursor.execute("PRAGMA table_info(produtos)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'estoque' in column_names:
            print("✅ Campo 'estoque' já existe na tabela produtos!")
            return True
        
        print("📝 Adicionando campo 'estoque' na tabela produtos...")
        
        # Adicionar o campo estoque
        cursor.execute("ALTER TABLE produtos ADD COLUMN estoque INTEGER DEFAULT 0")
        
        # Atualizar produtos existentes com estoque padrão (10 unidades)
        cursor.execute("UPDATE produtos SET estoque = 10 WHERE estoque IS NULL")
        
        # Commit das alterações
        conn.commit()
        
        print("✅ Campo 'estoque' adicionado com sucesso!")
        print("📊 Produtos existentes foram atualizados com estoque = 10")
        
        # Verificar resultado
        cursor.execute("PRAGMA table_info(produtos)")
        columns = cursor.fetchall()
        print("\n📋 Estrutura atual da tabela produtos:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - Default: {col[4]}")
        
        # Mostrar alguns produtos com estoque
        cursor.execute("SELECT id, nome, estoque FROM produtos LIMIT 5")
        produtos = cursor.fetchall()
        print(f"\n📦 Produtos com estoque (mostrando até 5):")
        for produto in produtos:
            print(f"  - ID {produto[0]}: {produto[1]} - Estoque: {produto[2]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao adicionar campo estoque: {e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    print("🍞 Adicionando campo 'estoque' na tabela produtos...")
    print("=" * 50)
    
    success = add_estoque_field()
    
    if success:
        print("\n🎉 Migração concluída com sucesso!")
        print("💡 Agora você pode:")
        print("  1. Iniciar o backend: python run_backend.py")
        print("  2. Iniciar o desktop: python run_desktop.py")
        print("  3. Iniciar o web: python run_web.py")
    else:
        print("\n❌ Falha na migração. Verifique os erros acima.") 