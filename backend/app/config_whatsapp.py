"""
Configurações para integração WhatsApp
"""

# Configurações do WhatsApp
WHATSAPP_CONFIG = {
    # Número do WhatsApp da padaria (formato: 5511999999999)
    "phone_number": "5511999999999",
    
    # Mensagem padrão de boas-vindas
    "welcome_message": "Olá! Bem-vindo à Padaria Delícias! 🥖✨\n\nComo posso ajudá-lo hoje?",
    
    # Mensagem para pedidos de entrega
    "delivery_message": "Olá! Gostaria de fazer um pedido de entrega.",
    
    # Mensagem para pedidos no local
    "local_message": "Olá! Gostaria de fazer um pedido para retirar no local.",
    
    # Horário de funcionamento
    "business_hours": {
        "monday": "6h às 22h",
        "tuesday": "6h às 22h", 
        "wednesday": "6h às 22h",
        "thursday": "6h às 22h",
        "friday": "6h às 22h",
        "saturday": "6h às 22h",
        "sunday": "6h às 22h"
    },
    
    # Informações de entrega
    "delivery_info": {
        "minimum_order": 15.00,  # Pedido mínimo para entrega
        "delivery_fee": 5.00,    # Taxa de entrega
        "delivery_time": "30-45 minutos",  # Tempo estimado de entrega
        "delivery_areas": [
            "Centro",
            "Bairro A",
            "Bairro B",
            "Bairro C"
        ]
    },
    
    # Formas de pagamento
    "payment_methods": [
        "Dinheiro",
        "PIX",
        "Cartão de crédito",
        "Cartão de débito"
    ]
}

# Templates de mensagens
MESSAGE_TEMPLATES = {
    "order_confirmation": """
✅ *PEDIDO CONFIRMADO*

Olá {customer_name}! Seu pedido foi recebido com sucesso.

📋 *Detalhes do Pedido:*
{order_details}

💰 *Total: R$ {total:.2f}*

🚚 *Informações de Entrega:*
• Endereço: {address}
• Telefone: {phone}
• Tempo estimado: {delivery_time}

💳 *Forma de Pagamento:* {payment_method}

Aguardamos sua confirmação! 🥖✨
    """,
    
    "order_status": """
📦 *STATUS DO PEDIDO*

Pedido #{order_id}

Status: {status}

{additional_info}

Em caso de dúvidas, entre em contato conosco.
    """,
    
    "menu_request": """
🍞 *CARDÁPIO DA PADARIA DELÍCIAS*

*PÃES:*
• Pão Francês - R$ 0,50
• Pão de Queijo - R$ 1,00
• Pão Integral - R$ 2,50
• Croissant - R$ 3,50

*BEBIDAS:*
• Café Expresso - R$ 2,00
• Cappuccino - R$ 4,50
• Suco Natural - R$ 3,00
• Água - R$ 1,50

*DOCES:*
• Brigadeiro - R$ 2,00
• Beijinho - R$ 2,00
• Bolo de Chocolate - R$ 15,00
• Torta de Limão - R$ 20,00

*SALGADOS:*
• Coxinha - R$ 3,50
• Pastel - R$ 2,50
• Empada - R$ 3,00
• Quibe - R$ 2,50

Para fazer seu pedido, envie os itens desejados! 🛒
    """,
    
    "business_hours": """
🕒 *HORÁRIO DE FUNCIONAMENTO*

*Segunda a Domingo:*
6h às 22h

📍 *Endereço:*
Rua das Flores, 123 - Centro

📞 *Telefone:*
(11) 99999-9999

Estamos sempre prontos para atendê-lo! 🥖✨
    """
}

def get_whatsapp_url(phone_number, message):
    """
    Gera URL do WhatsApp com mensagem pré-formatada
    
    Args:
        phone_number (str): Número do telefone
        message (str): Mensagem a ser enviada
    
    Returns:
        str: URL do WhatsApp
    """
    encoded_message = message.replace('\n', '%0A').replace(' ', '%20')
    return f"https://wa.me/{phone_number}?text={encoded_message}"

def format_order_message(order_data):
    """
    Formata mensagem de pedido para WhatsApp
    
    Args:
        order_data (dict): Dados do pedido
    
    Returns:
        str: Mensagem formatada
    """
    message = f"{WHATSAPP_CONFIG['delivery_message']}\n\n"
    message += "*PEDIDO:*\n"
    message += "━━━━━━━━━━━━━━━━━━━━\n"
    
    for item in order_data.get('items', []):
        message += f"• {item['name']} x{item['quantity']} - R$ {item['price']:.2f}\n"
    
    message += "━━━━━━━━━━━━━━━━━━━━\n"
    message += f"*TOTAL: R$ {order_data.get('total', 0):.2f}*\n\n"
    message += "Por favor, informe:\n"
    message += "• Nome completo\n"
    message += "• Endereço de entrega\n"
    message += "• Telefone para contato\n"
    message += "• Forma de pagamento\n\n"
    message += "Obrigado! 🥖✨"
    
    return message

def get_delivery_info():
    """
    Retorna informações de entrega
    
    Returns:
        dict: Informações de entrega
    """
    return WHATSAPP_CONFIG['delivery_info']

def get_payment_methods():
    """
    Retorna formas de pagamento disponíveis
    
    Returns:
        list: Lista de formas de pagamento
    """
    return WHATSAPP_CONFIG['payment_methods'] 