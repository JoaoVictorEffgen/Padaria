"""
Configurações centralizadas do sistema
"""
import os

# Configurações do Backend
BACKEND_HOST = "0.0.0.0"  # Aceita conexões de qualquer IP
BACKEND_PORT = 8000
BACKEND_URL = f"http://localhost:{BACKEND_PORT}"

# Configurações do Banco de Dados
DATABASE_URL = "sqlite:///database/padaria.db"
DATABASE_PATH = "database/padaria.db"

# Configurações de Rede
# Altere este IP para o IP da sua máquina na rede local
NETWORK_IP = "192.168.1.100"  # Exemplo - altere para seu IP
NETWORK_URL = f"http://{NETWORK_IP}:{BACKEND_PORT}"

# Configurações do Desktop
DESKTOP_REFRESH_INTERVAL = 5000  # 5 segundos

# Configurações do Tablet
TABLET_MESA_ID = 1  # Mesa padrão do tablet

# Categorias padrão de produtos
CATEGORIAS_PADRAO = [
    "Pães",
    "Bebidas", 
    "Cafés",
    "Doces",
    "Salgados"
]

# Produtos padrão para setup inicial
PRODUTOS_PADRAO = [
    {
        "nome": "Pão Francês",
        "preco": 0.50,
        "categoria": "Pães",
        "descricao": "Pão francês tradicional"
    },
    {
        "nome": "Pão de Queijo",
        "preco": 2.50,
        "categoria": "Pães", 
        "descricao": "Pão de queijo caseiro"
    },
    {
        "nome": "Croissant",
        "preco": 4.00,
        "categoria": "Pães",
        "descricao": "Croissant de manteiga"
    },
    {
        "nome": "Café Expresso",
        "preco": 3.50,
        "categoria": "Cafés",
        "descricao": "Café expresso tradicional"
    },
    {
        "nome": "Cappuccino",
        "preco": 5.00,
        "categoria": "Cafés",
        "descricao": "Cappuccino com espuma de leite"
    },
    {
        "nome": "Coca-Cola",
        "preco": 4.50,
        "categoria": "Bebidas",
        "descricao": "Refrigerante Coca-Cola 350ml"
    },
    {
        "nome": "Suco de Laranja",
        "preco": 6.00,
        "categoria": "Bebidas",
        "descricao": "Suco de laranja natural"
    },
    {
        "nome": "Brigadeiro",
        "preco": 3.00,
        "categoria": "Doces",
        "descricao": "Brigadeiro caseiro"
    },
    {
        "nome": "Pastel de Carne",
        "preco": 5.50,
        "categoria": "Salgados",
        "descricao": "Pastel de carne moída"
    },
    {
        "nome": "Coxinha",
        "preco": 4.50,
        "categoria": "Salgados",
        "descricao": "Coxinha de frango"
    }
]

# Mesas padrão
MESAS_PADRAO = [1, 2, 3, 4, 5]

def get_backend_url():
    """Retorna a URL do backend baseada no ambiente"""
    if os.getenv("PADARIA_NETWORK_MODE"):
        return NETWORK_URL
    return BACKEND_URL

def get_database_url():
    """Retorna a URL do banco de dados"""
    return DATABASE_URL

def create_database_directory():
    """Cria o diretório do banco se não existir"""
    os.makedirs("database", exist_ok=True) 