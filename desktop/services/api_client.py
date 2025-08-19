import requests
import json
from typing import List, Dict, Any

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Faz uma requisição para a API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                response = self.session.post(url, json=data)
            elif method == "PUT":
                response = self.session.put(url, json=data)
            elif method == "DELETE":
                response = self.session.delete(url)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None
    
    # Métodos para Mesas
    def listar_mesas(self) -> List[Dict]:
        """Lista todas as mesas"""
        return self._make_request("GET", "/mesas/") or []
    
    def criar_mesa(self, numero: int) -> Dict:
        """Cria uma nova mesa"""
        return self._make_request("POST", "/mesas/", {"numero": numero})
    
    def obter_mesa(self, mesa_id: int) -> Dict:
        """Obtém uma mesa específica"""
        return self._make_request("GET", f"/mesas/{mesa_id}")
    
    def gerar_qr_code_mesa(self, mesa_id: int) -> Dict:
        """Gera QR Code para uma mesa"""
        return self._make_request("GET", f"/mesas/{mesa_id}/qr-code")
    
    # Métodos para Produtos
    def listar_produtos(self) -> List[Dict]:
        """Lista todos os produtos"""
        return self._make_request("GET", "/produtos/") or []
    
    def listar_produtos_por_categoria(self, categoria: str) -> List[Dict]:
        """Lista produtos por categoria"""
        return self._make_request("GET", f"/produtos/categoria/{categoria}") or []
    
    def criar_produto(self, nome: str, preco: float, categoria: str, descricao: str = None, disponivel: bool = True) -> Dict:
        """Cria um novo produto"""
        data = {
            "nome": nome,
            "preco": preco,
            "categoria": categoria,
            "disponivel": disponivel
        }
        if descricao:
            data["descricao"] = descricao
        return self._make_request("POST", "/produtos/", data)
    
    def obter_produto(self, produto_id: int) -> Dict:
        """Obtém um produto específico"""
        return self._make_request("GET", f"/produtos/{produto_id}")
    
    def listar_categorias(self) -> List[str]:
        """Lista todas as categorias de produtos"""
        return self._make_request("GET", "/produtos/categorias/") or []
    
    # Métodos para Comandas
    def listar_comandas(self) -> List[Dict]:
        """Lista todas as comandas"""
        return self._make_request("GET", "/comandas/") or []
    
    def listar_comandas_abertas(self) -> List[Dict]:
        """Lista comandas abertas"""
        return self._make_request("GET", "/comandas/abertas/") or []
    
    def listar_comandas_para_impressao(self) -> List[Dict]:
        """Lista comandas que precisam ser impressas"""
        return self._make_request("GET", "/comandas/para-impressao/") or []
    
    def criar_comanda(self, mesa_id: int, observacoes: str = None) -> Dict:
        """Cria uma nova comanda"""
        data = {"mesa_id": mesa_id}
        if observacoes:
            data["observacoes"] = observacoes
        return self._make_request("POST", "/comandas/", data)
    
    def obter_comanda(self, comanda_id: int) -> Dict:
        """Obtém detalhes de uma comanda"""
        return self._make_request("GET", f"/comandas/{comanda_id}")
    
    def fechar_comanda(self, comanda_id: int) -> Dict:
        """Fecha uma comanda"""
        return self._make_request("PUT", f"/comandas/{comanda_id}/fechar")
    
    def finalizar_comanda(self, comanda_id: int) -> Dict:
        """Finaliza uma comanda (após pagamento)"""
        return self._make_request("PUT", f"/comandas/{comanda_id}/finalizar")
    
    def marcar_comanda_impressa(self, comanda_id: int) -> Dict:
        """Marca comanda como impressa"""
        return self._make_request("PUT", f"/comandas/{comanda_id}/imprimir")
    
    def adicionar_item_comanda(self, comanda_id: int, produto_id: int, quantidade: int, observacoes: str = None) -> Dict:
        """Adiciona um item à comanda"""
        data = {
            "produto_id": produto_id,
            "quantidade": quantidade,
            "preco_unitario": 0,  # Será calculado pelo backend
            "observacoes": observacoes,
            "status": "pendente"
        }
        return self._make_request("POST", f"/comandas/{comanda_id}/itens/", data)
    
    def listar_itens_comanda(self, comanda_id: int) -> List[Dict]:
        """Lista itens de uma comanda"""
        return self._make_request("GET", f"/comandas/{comanda_id}/itens/") or []
    
    def atualizar_status_item(self, item_id: int, status: str) -> Dict:
        """Atualiza status de um item"""
        return self._make_request("PUT", f"/itens/{item_id}/status?status={status}")
    
    def chamar_garcom(self, comanda_id: int, garcom_id: int = None) -> Dict:
        """Chama o garçom para uma mesa"""
        data = {}
        if garcom_id:
            data["garcom_id"] = garcom_id
        return self._make_request("POST", f"/comandas/{comanda_id}/chamar-garcom", data)
    
    def cancelar_comanda(self, comanda_id: int) -> Dict:
        """Cancela uma comanda (status = cancelado)"""
        return self._make_request("PUT", f"/comandas/{comanda_id}/cancelar")
    
    # Métodos para Garçons
    def listar_garcons(self) -> List[Dict]:
        """Lista todos os garçons"""
        return self._make_request("GET", "/garcons/") or []
    
    def criar_garcom(self, nome: str, codigo: str) -> Dict:
        """Cria um novo garçom"""
        return self._make_request("POST", "/garcons/", {"nome": nome, "codigo": codigo})
    
    def listar_atendimentos_garcom(self, garcom_id: int) -> List[Dict]:
        """Lista atendimentos de um garçom"""
        return self._make_request("GET", f"/garcons/{garcom_id}/atendimentos/") or []
    
    # Métodos para Sincronização Offline
    def sincronizar_offline(self, dispositivo_id: str, tipo_operacao: str, tabela: str, dados_json: str) -> Dict:
        """Registra operação para sincronização offline"""
        data = {
            "dispositivo_id": dispositivo_id,
            "tipo_operacao": tipo_operacao,
            "tabela": tabela,
            "dados_json": dados_json
        }
        return self._make_request("POST", "/sincronizacao/", data)
    
    def listar_sincronizacoes_pendentes(self) -> List[Dict]:
        """Lista sincronizações pendentes"""
        return self._make_request("GET", "/sincronizacao/pendentes/") or []
    
    def marcar_sincronizada(self, sinc_id: int) -> Dict:
        """Marca sincronização como concluída"""
        return self._make_request("PUT", f"/sincronizacao/{sinc_id}/marcar-sincronizada")
    
    # Métodos para Menu Público
    def obter_menu_publico(self, mesa_id: int) -> Dict:
        """Obtém menu público para QR Code"""
        return self._make_request("GET", f"/menu/{mesa_id}")
    
    # Métodos para Pedidos Online
    def listar_pedidos_online(self) -> List[Dict]:
        """Lista todos os pedidos online"""
        return self._make_request("GET", "/pedidos-online/") or []
    
    def obter_pedido_online(self, pedido_id: int) -> Dict:
        """Obtém detalhes de um pedido online"""
        return self._make_request("GET", f"/pedidos-online/{pedido_id}")
    
    def atualizar_status_pedido_online(self, pedido_id: int, status: str) -> Dict:
        """Atualiza status de um pedido online"""
        return self._make_request("PUT", f"/pedidos-online/{pedido_id}/status?status={status}")
    
    def criar_pedido_online(self, nome_cliente: str, telefone: str, endereco: str, 
                           forma_pagamento: str, itens: List[Dict], observacoes: str = None) -> Dict:
        """Cria um novo pedido online"""
        data = {
            "nome_cliente": nome_cliente,
            "telefone": telefone,
            "endereco": endereco,
            "forma_pagamento": forma_pagamento,
            "itens": itens,
            "observacoes": observacoes
        }
        return self._make_request("POST", "/pedidos-online/", data)
    
    # ============================================================================
    # MÉTODOS PARA CLIENTES
    # ============================================================================
    
    def listar_clientes(self) -> List[Dict]:
        """Lista todos os clientes"""
        return self._make_request("GET", "/clientes/") or []
    
    def obter_cliente(self, cliente_id: int) -> Dict:
        """Obtém um cliente específico"""
        return self._make_request("GET", f"/clientes/{cliente_id}")
    
    def obter_cliente_por_telefone(self, telefone: str) -> Dict:
        """Obtém cliente por telefone"""
        return self._make_request("GET", f"/clientes/telefone/{telefone}")
    
    def criar_cliente(self, nome: str, telefone: str, endereco: str) -> Dict:
        """Cria um novo cliente"""
        data = {
            "nome": nome,
            "telefone": telefone,
            "endereco": endereco
        }
        return self._make_request("POST", "/clientes/", data)
    
    # ============================================================================
    # MÉTODOS PARA RESERVAS
    # ============================================================================
    
    def listar_reservas(self) -> List[Dict]:
        """Lista todas as reservas ativas"""
        return self._make_request("GET", "/reservas/") or []
    
    def obter_reserva(self, reserva_id: int) -> Dict:
        """Obtém uma reserva específica"""
        return self._make_request("GET", f"/reservas/{reserva_id}")
    
    def obter_reservas_mesa(self, mesa_id: int) -> Dict:
        """Obtém reservas de uma mesa específica"""
        return self._make_request("GET", f"/reservas/mesa/{mesa_id}")
    
    def criar_reserva(self, mesa_id: int, cliente_id: int, data_reserva: str, 
                     horario_reserva: str, observacoes: str = None) -> Dict:
        """Cria uma nova reserva"""
        data = {
            "mesa_id": mesa_id,
            "cliente_id": cliente_id,
            "data_reserva": data_reserva,
            "horario_reserva": horario_reserva
        }
        if observacoes:
            data["observacoes"] = observacoes
        return self._make_request("POST", "/reservas/", data)
    
    def cancelar_reserva(self, reserva_id: int) -> Dict:
        """Cancela uma reserva"""
        return self._make_request("PUT", f"/reservas/{reserva_id}/cancelar") 