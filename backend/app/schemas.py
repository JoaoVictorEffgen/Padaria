from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Schemas para Mesa
class MesaBase(BaseModel):
    numero: int

class MesaCreate(MesaBase):
    pass

class Mesa(MesaBase):
    id: int
    status: str
    qr_code: Optional[str] = None
    
    class Config:
        from_attributes = True

# Schemas para Produto
class ProdutoBase(BaseModel):
    nome: str
    preco: float
    categoria: str
    descricao: Optional[str] = None
    disponivel: bool = True

class ProdutoCreate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    id: int
    
    class Config:
        from_attributes = True

# Schemas para ItemComanda
class ItemComandaBase(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float
    observacoes: Optional[str] = None
    status: str = "pendente"

class ItemComandaCreate(ItemComandaBase):
    pass

class ItemComanda(ItemComandaBase):
    id: int
    comanda_id: int
    produto: Produto
    
    class Config:
        from_attributes = True

# Schemas para Comanda
class ComandaBase(BaseModel):
    mesa_id: int
    observacoes: Optional[str] = None
    chamando_garcom: Optional[bool] = False

class ComandaCreate(ComandaBase):
    pass

class Comanda(ComandaBase):
    id: int
    status: str
    total: float
    data_abertura: datetime
    data_fechamento: Optional[datetime] = None
    data_impressao: Optional[datetime] = None
    mesa: Mesa
    itens: List[ItemComanda] = []
    
    class Config:
        from_attributes = True

# Schemas para respostas da API
class ComandaResumo(BaseModel):
    id: int
    mesa_numero: int
    status: str
    total: float
    data_abertura: datetime
    quantidade_itens: int
    chamando_garcom: Optional[bool] = False
    
    class Config:
        from_attributes = True

# Schemas para Garçom
class GarcomBase(BaseModel):
    nome: str
    codigo: str

class GarcomCreate(GarcomBase):
    pass

class Garcom(GarcomBase):
    id: int
    ativo: bool
    
    class Config:
        from_attributes = True

# Schemas para Atendimento Garçom
class AtendimentoGarcomBase(BaseModel):
    garcom_id: int
    comanda_id: int
    tipo: str

class AtendimentoGarcomCreate(AtendimentoGarcomBase):
    pass

class AtendimentoGarcom(AtendimentoGarcomBase):
    id: int
    data_atendimento: datetime
    garcom: Garcom
    
    class Config:
        from_attributes = True

# Schemas para Sincronização Offline
class SincronizacaoOfflineBase(BaseModel):
    dispositivo_id: str
    tipo_operacao: str
    tabela: str
    dados_json: str

class SincronizacaoOfflineCreate(SincronizacaoOfflineBase):
    pass

class SincronizacaoOffline(SincronizacaoOfflineBase):
    id: int
    data_criacao: datetime
    sincronizado: bool
    data_sincronizacao: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Schemas para Impressão
class ComandaImpressao(BaseModel):
    id: int
    mesa_numero: int
    data_abertura: datetime
    total: float
    observacoes: Optional[str] = None
    itens: List[ItemComanda] = []
    
    class Config:
        from_attributes = True

# Schemas para QR Code
class QRCodeResponse(BaseModel):
    mesa_id: int
    mesa_numero: int
    qr_code_url: str
    menu_url: str

# Schemas para Pedidos Online
class ItemPedidoOnlineBase(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float
    observacoes: Optional[str] = None

class ItemPedidoOnlineCreate(ItemPedidoOnlineBase):
    pass

class ItemPedidoOnline(ItemPedidoOnlineBase):
    id: int
    pedido_id: int
    produto: Produto
    
    class Config:
        from_attributes = True

class PedidoOnlineBase(BaseModel):
    nome_cliente: str
    telefone: str
    endereco: str
    forma_pagamento: str
    observacoes: Optional[str] = None

class PedidoOnlineCreate(PedidoOnlineBase):
    itens: List[ItemPedidoOnlineCreate]

class PedidoOnline(PedidoOnlineBase):
    id: int
    total: float
    status: str
    data_pedido: datetime
    data_confirmacao: Optional[datetime] = None
    data_entrega: Optional[datetime] = None
    whatsapp_enviado: bool
    itens: List[ItemPedidoOnline] = []
    
    class Config:
        from_attributes = True

class PedidoOnlineResumo(BaseModel):
    id: int
    nome_cliente: str
    telefone: str
    total: float
    status: str
    data_pedido: datetime
    quantidade_itens: int
    
    class Config:
        from_attributes = True 