import requests

# Verificar detalhes do pedido #2 (Maria Santos)
print("=== DETALHES DO PEDIDO #2 ===")
pedido = requests.get('http://localhost:8000/pedidos-online/2').json()
print(f"Cliente: {pedido['nome_cliente']}")
print(f"Total: R$ {pedido['total']}")
print(f"Status: {pedido['status']}")
print("\nItens:")
for item in pedido['itens']:
    print(f"  - {item['quantidade']}x {item['produto']['nome']} (R$ {item['preco_unitario']} cada) = R$ {item['quantidade'] * item['preco_unitario']}")

print(f"\nTotal calculado: R$ {sum(item['quantidade'] * item['preco_unitario'] for item in pedido['itens'])}")
print(f"Total do pedido: R$ {pedido['total']}") 