import sqlite3
import sys

DB_PATH = 'backend/database/padaria.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Verifica se a coluna já existe
cursor.execute("PRAGMA table_info(comandas)")
columns = [col[1] for col in cursor.fetchall()]

if 'chamando_garcom' not in columns:
    try:
        cursor.execute("ALTER TABLE comandas ADD COLUMN chamando_garcom BOOLEAN DEFAULT 0")
        print('Coluna chamando_garcom adicionada com sucesso!')
    except Exception as e:
        print(f'Erro ao adicionar coluna: {e}')
else:
    print('Coluna chamando_garcom já existe.')

conn.commit()
conn.close() 