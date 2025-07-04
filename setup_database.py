#!/usr/bin/env python3
"""
Script para configurar o banco de dados com dados iniciais
"""
import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.join(os.getcwd(), "backend"))

from app.database import engine, SessionLocal
from app.models import Base, Mesa, Produto
from app.schemas import MesaCreate, ProdutoCreate

def criar_tabelas():
    """Cria as tabelas no banco de dados"""
    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

def inserir_dados_iniciais():
    """Insere dados iniciais no banco"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem dados
        if db.query(Mesa).count() > 0:
            print("Dados já existem no banco. Pulando inserção...")
            return
        
        print("Inserindo dados iniciais...")
        
        # Criar mesas
        mesas = [
            MesaCreate(numero=1),
            MesaCreate(numero=2),
            MesaCreate(numero=3),
            MesaCreate(numero=4),
            MesaCreate(numero=5),
        ]
        
        for mesa_data in mesas:
            mesa = Mesa(**mesa_data.dict())
            db.add(mesa)
        
        # Criar produtos
        produtos = [
            ProdutoCreate(
                nome="Pão Francês",
                preco=0.50,
                categoria="Pães",
                descricao="Pão francês tradicional"
            ),
            ProdutoCreate(
                nome="Pão de Queijo",
                preco=2.50,
                categoria="Pães",
                descricao="Pão de queijo caseiro"
            ),
            ProdutoCreate(
                nome="Croissant",
                preco=4.00,
                categoria="Pães",
                descricao="Croissant de manteiga"
            ),
            ProdutoCreate(
                nome="Café Expresso",
                preco=3.50,
                categoria="Cafés",
                descricao="Café expresso tradicional"
            ),
            ProdutoCreate(
                nome="Cappuccino",
                preco=5.00,
                categoria="Cafés",
                descricao="Cappuccino com espuma de leite"
            ),
            ProdutoCreate(
                nome="Coca-Cola",
                preco=4.50,
                categoria="Bebidas",
                descricao="Refrigerante Coca-Cola 350ml"
            ),
            ProdutoCreate(
                nome="Suco de Laranja",
                preco=6.00,
                categoria="Bebidas",
                descricao="Suco de laranja natural"
            ),
            ProdutoCreate(
                nome="Brigadeiro",
                preco=3.00,
                categoria="Doces",
                descricao="Brigadeiro caseiro"
            ),
            ProdutoCreate(
                nome="Pastel de Carne",
                preco=5.50,
                categoria="Salgados",
                descricao="Pastel de carne moída"
            ),
            ProdutoCreate(
                nome="Coxinha",
                preco=4.50,
                categoria="Salgados",
                descricao="Coxinha de frango"
            ),
        ]
        
        for produto_data in produtos:
            produto = Produto(**produto_data.dict())
            db.add(produto)
        
        db.commit()
        print("Dados iniciais inseridos com sucesso!")
        
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    print("=== Configuração do Banco de Dados ===")
    
    # Criar tabelas
    criar_tabelas()
    
    # Inserir dados iniciais
    inserir_dados_iniciais()
    
    print("Configuração concluída!")

if __name__ == "__main__":
    main() 