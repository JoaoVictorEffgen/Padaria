import requests

# Verificar produtos
print("=== PRODUTOS DISPONÍVEIS ===")
produtos = requests.get('http://localhost:8000/produtos/').json()
for p in produtos:
    print(f"ID: {p['id']}, Nome: {p['nome']}, Preço: R$ {p['preco']}")

print("\n=== PEDIDOS ONLINE ===")
pedidos = requests.get('http://localhost:8000/pedidos-online/').json()
for p in pedidos:
    print(f"ID: {p['id']}, Cliente: {p['nome_cliente']}, Total: R$ {p['total']}, Itens: {p['quantidade_itens']}") 