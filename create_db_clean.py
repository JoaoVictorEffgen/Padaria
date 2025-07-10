import sqlite3
import os

# Caminho do banco de dados
db_path = "backend/database/padaria.db"

# Garantir que o diretório existe
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Conectar ao banco de dados
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🗄️ Criando banco de dados limpo...")

# Criar tabelas sem o campo estoque
cursor.execute('''
CREATE TABLE IF NOT EXISTS mesas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER UNIQUE NOT NULL,
    status TEXT DEFAULT 'livre',
    qr_code TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    categoria TEXT NOT NULL,
    descricao TEXT,
    disponivel BOOLEAN DEFAULT 1
)
''')

cursor.execute('''
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
''')

cursor.execute('''
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
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS garcons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    codigo TEXT UNIQUE NOT NULL,
    ativo BOOLEAN DEFAULT 1
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS atendimentos_garcom (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    garcom_id INTEGER NOT NULL,
    comanda_id INTEGER NOT NULL,
    data_atendimento DATETIME DEFAULT CURRENT_TIMESTAMP,
    tipo TEXT NOT NULL,
    FOREIGN KEY (garcom_id) REFERENCES garcons (id),
    FOREIGN KEY (comanda_id) REFERENCES comandas (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS sincronizacoes_offline (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dispositivo_id TEXT NOT NULL,
    tipo_operacao TEXT NOT NULL,
    tabela TEXT NOT NULL,
    dados_json TEXT NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    sincronizado BOOLEAN DEFAULT 0,
    data_sincronizacao DATETIME
)
''')

cursor.execute('''
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
''')

cursor.execute('''
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
''')

print("✅ Tabelas criadas com sucesso!")

# Inserir dados de exemplo
print("📝 Inserindo dados de exemplo...")

# Mesas
mesas = [
    (1, 'livre'),
    (2, 'livre'),
    (3, 'livre'),
    (4, 'livre'),
    (5, 'livre')
]

cursor.executemany('INSERT INTO mesas (numero, status) VALUES (?, ?)', mesas)

# Produtos
produtos = [
    ('Pão Francês', 0.50, 'Pães', 'Pão francês tradicional'),
    ('Croissant', 3.50, 'Pães', 'Croissant de manteiga'),
    ('Bolo de Chocolate', 25.00, 'Bolos', 'Bolo de chocolate caseiro'),
    ('Café Expresso', 2.50, 'Bebidas', 'Café expresso forte'),
    ('Cappuccino', 4.00, 'Bebidas', 'Cappuccino cremoso'),
    ('Sanduíche Natural', 8.00, 'Sanduíches', 'Sanduíche de frango'),
    ('Torta de Maçã', 15.00, 'Sobremesas', 'Torta de maçã caseira'),
    ('Suco de Laranja', 5.00, 'Bebidas', 'Suco natural de laranja'),
    ('Pão de Queijo', 2.00, 'Pães', 'Pão de queijo mineiro'),
    ('Brigadeiro', 1.50, 'Doces', 'Brigadeiro caseiro')
]

cursor.executemany('INSERT INTO produtos (nome, preco, categoria, descricao) VALUES (?, ?, ?, ?)', produtos)

# Garçons
garcons = [
    ('João Silva', 'G001'),
    ('Maria Santos', 'G002'),
    ('Pedro Costa', 'G003')
]

cursor.executemany('INSERT INTO garcons (nome, codigo) VALUES (?, ?)', garcons)

print("✅ Dados de exemplo inseridos!")

# Commit das alterações
conn.commit()
conn.close()

print("🎉 Banco de dados criado com sucesso!")
print("📍 Localização: backend/database/padaria.db")
print("📊 Tabelas criadas: mesas, produtos, comandas, itens_comanda, garcons, atendimentos_garcom, sincronizacoes_offline, pedidos_online, itens_pedido_online")
print("📝 Dados inseridos: 5 mesas, 10 produtos, 3 garçons") 