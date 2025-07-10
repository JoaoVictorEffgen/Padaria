import sqlite3

try:
    conn = sqlite3.connect('backend/database/padaria.db')
    cursor = conn.cursor()
    
    # Verificar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Tabelas no banco:", tables)
    
    # Se a tabela produtos existe, verificar estrutura
    if ('produtos',) in tables:
        cursor.execute("PRAGMA table_info(produtos)")
        columns = cursor.fetchall()
        print("\nEstrutura da tabela produtos:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    
    conn.close()
except Exception as e:
    print(f"Erro: {e}") 