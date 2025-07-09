"""
Configuração e serviço para integração com WhatsApp
"""

import requests
import json
from datetime import datetime
from typing import List, Dict

class WhatsAppService:
    def __init__(self):
        # Configurações do WhatsApp Business API
        # Você pode usar serviços como Twilio, MessageBird, ou WhatsApp Business API
        self.api_url = "https://api.whatsapp.com/v1/messages"  # Exemplo
        self.phone_number = "5511999999999"  # Número da padaria
        self.api_key = "sua_api_key_aqui"  # Sua chave da API
        
    def enviar_pedido_whatsapp(self, pedido: Dict) -> bool:
        """
        Envia pedido para o WhatsApp da padaria
        """
        try:
            # Formatar mensagem do pedido
            mensagem = self._formatar_mensagem_pedido(pedido)
            
            # Enviar via API do WhatsApp
            # Nota: Esta é uma implementação de exemplo
            # Você precisará configurar uma API real do WhatsApp
            
            payload = {
                "to": self.phone_number,
                "type": "text",
                "text": {
                    "body": mensagem
                }
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Comentado para não enviar mensagens reais durante desenvolvimento
            # response = requests.post(self.api_url, json=payload, headers=headers)
            
            # Para desenvolvimento, apenas simular o envio
            print(f"[WHATSAPP] Mensagem enviada para {self.phone_number}")
            print(f"[WHATSAPP] Conteúdo: {mensagem}")
            
            return True
            
        except Exception as e:
            print(f"[ERRO] Falha ao enviar WhatsApp: {e}")
            return False
    
    def _formatar_mensagem_pedido(self, pedido: Dict) -> str:
        """
        Formata a mensagem do pedido para WhatsApp
        """
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        mensagem = f"""
🍞 *NOVO PEDIDO ONLINE - Padaria Delícias*

📅 Data/Hora: {data_hora}
🆔 Pedido #: {pedido['id']}

👤 *CLIENTE:*
Nome: {pedido['nome_cliente']}
Telefone: {pedido['telefone']}
Endereço: {pedido['endereco']}

💳 *FORMA DE PAGAMENTO:*
{pedido['forma_pagamento'].upper()}

🛒 *ITENS DO PEDIDO:*
"""
        
        # Adicionar itens
        for item in pedido['itens']:
            subtotal = item['quantidade'] * item['preco_unitario']
            mensagem += f"• {item['quantidade']}x {item['produto']['nome']} - R$ {subtotal:.2f}\n"
        
        mensagem += f"""
💰 *TOTAL: R$ {pedido['total']:.2f}*

📝 *OBSERVAÇÕES:*
{pedido.get('observacoes', 'Nenhuma observação')}

---
*Este pedido foi feito através do site da padaria*
        """
        
        return mensagem.strip()
    
    def enviar_confirmacao_cliente(self, pedido: Dict) -> bool:
        """
        Envia confirmação do pedido para o cliente
        """
        try:
            mensagem = f"""
🍞 *Pedido Confirmado - Padaria Delícias*

Olá {pedido['nome_cliente']}! 

Seu pedido #{pedido['id']} foi recebido e está sendo preparado.

📋 *Resumo do Pedido:*
Total: R$ {pedido['total']:.2f}
Forma de Pagamento: {pedido['forma_pagamento'].upper()}

⏰ Tempo estimado de entrega: 30-45 minutos

📞 Em caso de dúvidas, entre em contato: (11) 99999-9999

Obrigado por escolher a Padaria Delícias! 🥖
            """
            
            # Enviar para o cliente
            # Implementar envio real aqui
            
            print(f"[WHATSAPP] Confirmação enviada para {pedido['telefone']}")
            return True
            
        except Exception as e:
            print(f"[ERRO] Falha ao enviar confirmação: {e}")
            return False

# Instância global do serviço
whatsapp_service = WhatsAppService() 