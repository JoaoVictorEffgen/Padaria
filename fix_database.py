import sqlite3
import os

DB_PATH = 'backend/database/padaria.db'

def fix_database():
    print("🔧 Corrigindo banco de dados...")
    
    # Fazer backup do banco atual
    backup_path = DB_PATH + '.backup'
    if os.path.exists(DB_PATH):
        import shutil
        shutil.copy2(DB_PATH, backup_path)
        print(f"✅ Backup criado: {backup_path}")
    
    # Conectar ao banco
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verificar se a coluna existe
    cursor.execute("PRAGMA table_info(comandas)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'chamando_garcom' not in columns:
        print("❌ Coluna chamando_garcom não existe. Adicionando...")
        try:
            cursor.execute("ALTER TABLE comandas ADD COLUMN chamando_garcom BOOLEAN DEFAULT 0")
            print("✅ Coluna chamando_garcom adicionada!")
        except Exception as e:
            print(f"❌ Erro ao adicionar coluna: {e}")
    else:
        print("✅ Coluna chamando_garcom já existe!")
    
    # Verificar se há dados na tabela
    cursor.execute("SELECT COUNT(*) FROM comandas")
    count = cursor.fetchone()[0]
    print(f"📊 Comandas no banco: {count}")
    
    # Verificar estrutura final
    cursor.execute("PRAGMA table_info(comandas)")
    final_columns = [col[1] for col in cursor.fetchall()]
    print(f"📋 Colunas finais: {final_columns}")
    
    conn.commit()
    conn.close()
    
    print("✅ Banco de dados corrigido!")
    return True

if __name__ == "__main__":
    fix_database() 