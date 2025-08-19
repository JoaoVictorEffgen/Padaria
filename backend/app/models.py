from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Mesa(Base):
    __tablename__ = "mesas"
    
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, index=True)
    status = Column(String, default="livre")  # livre, ocupada, reservada
    qr_code = Column(String, nullable=True)  # URL do QR Code
    
    comandas = relationship("Comanda", back_populates="mesa")
    reservas = relationship("Reserva", back_populates="mesa")

class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    preco = Column(Float)
    categoria = Column(String, index=True)
    descricao = Column(Text, nullable=True)
    disponivel = Column(Boolean, default=True)  # Para controle de estoque
    
    itens = relationship("ItemComanda", back_populates="produto")

class Comanda(Base):
    __tablename__ = "comandas"
    
    id = Column(Integer, primary_key=True, index=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"))
    status = Column(String, default="aberta")  # aberta, aguardando_pagamento, fechada, impressa
    total = Column(Float, default=0.0)
    data_abertura = Column(DateTime(timezone=True), server_default=func.now())
    data_fechamento = Column(DateTime(timezone=True), nullable=True)
    data_impressao = Column(DateTime(timezone=True), nullable=True)
    observacoes = Column(Text, nullable=True)  # Observações especiais
    chamando_garcom = Column(Boolean, default=False)  # Novo campo
    
    mesa = relationship("Mesa", back_populates="comandas")
    itens = relationship("ItemComanda", back_populates="comanda")

class ItemComanda(Base):
    __tablename__ = "itens_comanda"
    
    id = Column(Integer, primary_key=True, index=True)
    comanda_id = Column(Integer, ForeignKey("comandas.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer, default=1)
    preco_unitario = Column(Float)
    observacoes = Column(Text, nullable=True)  # Observações do item
    status = Column(String, default="pendente")  # pendente, preparando, pronto
    
    comanda = relationship("Comanda", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")

class Garcom(Base):
    __tablename__ = "garcons"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    codigo = Column(String, unique=True, index=True)
    ativo = Column(Boolean, default=True)
    
    atendimentos = relationship("AtendimentoGarcom", back_populates="garcom")

class AtendimentoGarcom(Base):
    __tablename__ = "atendimentos_garcom"
    
    id = Column(Integer, primary_key=True, index=True)
    garcom_id = Column(Integer, ForeignKey("garcons.id"))
    comanda_id = Column(Integer, ForeignKey("comandas.id"))
    data_atendimento = Column(DateTime(timezone=True), server_default=func.now())
    tipo = Column(String)  # chamada, entrega, fechamento
    
    garcom = relationship("Garcom", back_populates="atendimentos")

class SincronizacaoOffline(Base):
    __tablename__ = "sincronizacoes_offline"
    
    id = Column(Integer, primary_key=True, index=True)
    dispositivo_id = Column(String, index=True)
    tipo_operacao = Column(String)  # create, update, delete
    tabela = Column(String)  # comandas, itens_comanda, etc.
    dados_json = Column(Text)  # Dados da operação
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    sincronizado = Column(Boolean, default=False)
    data_sincronizacao = Column(DateTime(timezone=True), nullable=True)

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    telefone = Column(String, unique=True, index=True)
    endereco = Column(Text)
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())
    
    reservas = relationship("Reserva", back_populates="cliente")

class Reserva(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, index=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"))
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    data_reserva = Column(DateTime(timezone=True), nullable=False)
    horario_reserva = Column(String, nullable=False)  # formato "HH:MM"
    status = Column(String, default="ativa")  # ativa, cancelada, finalizada
    observacoes = Column(Text, nullable=True)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    
    mesa = relationship("Mesa", back_populates="reservas")
    cliente = relationship("Cliente", back_populates="reservas")

class PedidoOnline(Base):
    __tablename__ = "pedidos_online"
    
    id = Column(Integer, primary_key=True, index=True)
    nome_cliente = Column(String, index=True)
    telefone = Column(String, index=True)
    endereco = Column(Text)
    forma_pagamento = Column(String)  # dinheiro, cartao, pix, transferencia
    total = Column(Float)
    status = Column(String, default="pendente")  # pendente, confirmado, preparando, entregando, entregue, cancelado
    observacoes = Column(Text, nullable=True)
    data_pedido = Column(DateTime(timezone=True), server_default=func.now())
    data_confirmacao = Column(DateTime(timezone=True), nullable=True)
    data_entrega = Column(DateTime(timezone=True), nullable=True)
    whatsapp_enviado = Column(Boolean, default=False)
    
    itens = relationship("ItemPedidoOnline", back_populates="pedido")

class ItemPedidoOnline(Base):
    __tablename__ = "itens_pedido_online"
    
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos_online.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer, default=1)
    preco_unitario = Column(Float)
    observacoes = Column(Text, nullable=True)
    
    pedido = relationship("PedidoOnline", back_populates="itens")
    produto = relationship("Produto") 