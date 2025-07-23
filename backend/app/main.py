from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import qrcode
import json
import uuid
from io import BytesIO
import base64
import os

from . import models, schemas
from .database import engine, get_db

# Criar tabelas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Padaria API", version="2.0.0")

# Configurações
BASE_URL = "http://localhost:8000"

# Servir arquivos estáticos
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Endpoints para Mesas
@app.get("/mesas/", response_model=List[schemas.Mesa])
def listar_mesas(db: Session = Depends(get_db)):
    return db.query(models.Mesa).all()

@app.post("/mesas/", response_model=schemas.Mesa)
def criar_mesa(mesa: schemas.MesaCreate, db: Session = Depends(get_db)):
    db_mesa = models.Mesa(**mesa.dict())
    db.add(db_mesa)
    db.commit()
    db.refresh(db_mesa)
    return db_mesa

@app.get("/mesas/{mesa_id}", response_model=schemas.Mesa)
def obter_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = db.query(models.Mesa).filter(models.Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    return mesa

@app.get("/mesas/{mesa_id}/qr-code", response_model=schemas.QRCodeResponse)
def gerar_qr_code_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = db.query(models.Mesa).filter(models.Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    
    # Gerar QR Code
    menu_url = f"{BASE_URL}/menu/{mesa_id}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(menu_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return schemas.QRCodeResponse(
        mesa_id=mesa.id,
        mesa_numero=mesa.numero,
        qr_code_url=f"data:image/png;base64,{qr_code_base64}",
        menu_url=menu_url
    )

@app.put("/mesas/{mesa_id}/reservar")
def reservar_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = db.query(models.Mesa).filter(models.Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    if mesa.status == "ocupada":
        raise HTTPException(status_code=400, detail="Mesa já está ocupada")
    mesa.status = "reservada"
    db.commit()
    return {"message": "Mesa reservada com sucesso"}

@app.put("/mesas/{mesa_id}/liberar")
def liberar_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = db.query(models.Mesa).filter(models.Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    mesa.status = "livre"
    db.commit()
    return {"message": "Mesa liberada com sucesso"}

# Endpoints para Produtos
@app.get("/produtos/", response_model=List[schemas.Produto])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(models.Produto).filter(models.Produto.disponivel == True).all()

@app.get("/produtos/categoria/{categoria}", response_model=List[schemas.Produto])
def listar_produtos_por_categoria(categoria: str, db: Session = Depends(get_db)):
    return db.query(models.Produto).filter(
        models.Produto.categoria == categoria,
        models.Produto.disponivel == True
    ).all()

@app.post("/produtos/", response_model=schemas.Produto)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = models.Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@app.get("/produtos/{produto_id}", response_model=schemas.Produto)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

# Endpoints para Comandas
@app.get("/comandas/", response_model=List[schemas.ComandaResumo])
def listar_comandas(db: Session = Depends(get_db)):
    comandas = db.query(models.Comanda).all()
    resultado = []
    for comanda in comandas:
        resultado.append(schemas.ComandaResumo(
            id=comanda.id,
            mesa_numero=comanda.mesa.numero,
            status=comanda.status,
            total=comanda.total,
            data_abertura=comanda.data_abertura,
            quantidade_itens=len(comanda.itens)
        ))
    return resultado

@app.get("/comandas/abertas/", response_model=List[schemas.ComandaResumo])
def listar_comandas_abertas(db: Session = Depends(get_db)):
    comandas = db.query(models.Comanda).filter(models.Comanda.status == "aberta").all()
    resultado = []
    for comanda in comandas:
        resultado.append(schemas.ComandaResumo(
            id=comanda.id,
            mesa_numero=comanda.mesa.numero,
            status=comanda.status,
            total=comanda.total,
            data_abertura=comanda.data_abertura,
            quantidade_itens=len(comanda.itens)
        ))
    return resultado

@app.get("/comandas/para-impressao/", response_model=List[schemas.ComandaImpressao])
def listar_comandas_para_impressao(db: Session = Depends(get_db)):
    """Comandas que precisam ser impressas na cozinha"""
    comandas = db.query(models.Comanda).filter(
        models.Comanda.status.in_(["aberta", "impressa"])
    ).all()
    
    resultado = []
    for comanda in comandas:
        resultado.append(schemas.ComandaImpressao(
            id=comanda.id,
            mesa_numero=comanda.mesa.numero,
            data_abertura=comanda.data_abertura,
            total=comanda.total,
            observacoes=comanda.observacoes,
            itens=comanda.itens
        ))
    return resultado

@app.post("/comandas/", response_model=schemas.Comanda)
def criar_comanda(comanda: schemas.ComandaCreate, db: Session = Depends(get_db)):
    # Verificar se a mesa existe
    mesa = db.query(models.Mesa).filter(models.Mesa.id == comanda.mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    
    # Verificar se já existe comanda aberta para esta mesa
    comanda_existente = db.query(models.Comanda).filter(
        models.Comanda.mesa_id == comanda.mesa_id,
        models.Comanda.status == "aberta"
    ).first()
    
    if comanda_existente:
        raise HTTPException(status_code=400, detail="Já existe comanda aberta para esta mesa")
    
    db_comanda = models.Comanda(**comanda.dict())
    db.add(db_comanda)
    
    # Atualizar status da mesa
    mesa.status = "ocupada"
    
    db.commit()
    db.refresh(db_comanda)
    return db_comanda

@app.get("/comandas/{comanda_id}", response_model=schemas.Comanda)
def obter_comanda(comanda_id: int, db: Session = Depends(get_db)):
    comanda = db.query(models.Comanda).filter(models.Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    return comanda

@app.put("/comandas/{comanda_id}/fechar")
def fechar_comanda(comanda_id: int, db: Session = Depends(get_db)):
    comanda = db.query(models.Comanda).filter(models.Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    
    comanda.status = "aguardando_pagamento"
    comanda.data_fechamento = datetime.now()
    
    # Liberar mesa
    mesa = comanda.mesa
    mesa.status = "livre"
    
    db.commit()
    return {"message": "Comanda fechada com sucesso"}

@app.put("/comandas/{comanda_id}/finalizar")
def finalizar_comanda(comanda_id: int, db: Session = Depends(get_db)):
    comanda = db.query(models.Comanda).filter(models.Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    
    comanda.status = "fechada"
    db.commit()
    return {"message": "Comanda finalizada com sucesso"}

@app.put("/comandas/{comanda_id}/imprimir")
def marcar_comanda_impressa(comanda_id: int, db: Session = Depends(get_db)):
    comanda = db.query(models.Comanda).filter(models.Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    
    comanda.status = "impressa"
    comanda.data_impressao = datetime.now()
    db.commit()
    return {"message": "Comanda marcada como impressa"}

@app.put("/comandas/{comanda_id}/cancelar")
def cancelar_comanda(comanda_id: int, db: Session = Depends(get_db)):
    comanda = db.query(models.Comanda).filter(models.Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    comanda.status = "cancelado"
    db.commit()
    return {"message": "Comanda cancelada com sucesso"}

# Endpoints para Itens da Comanda
@app.post("/comandas/{comanda_id}/itens/", response_model=schemas.ItemComanda)
def adicionar_item_comanda(
    comanda_id: int, 
    item: schemas.ItemComandaCreate, 
    db: Session = Depends(get_db)
):
    # Verificar se a comanda existe e está aberta
    comanda = db.query(models.Comanda).filter(models.Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    
    if comanda.status not in ["aberta", "impressa"]:
        raise HTTPException(status_code=400, detail="Comanda não está aberta")
    
    # Verificar se o produto existe
    produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    if not produto.disponivel:
        raise HTTPException(status_code=400, detail="Produto não disponível")
    

    
    # Criar item da comanda
    db_item = models.ItemComanda(
        comanda_id=comanda_id,
        produto_id=item.produto_id,
        quantidade=item.quantidade,
        preco_unitario=produto.preco,
        observacoes=item.observacoes,
        status=item.status
    )
    db.add(db_item)
    
    # Atualizar total da comanda
    comanda.total += (produto.preco * item.quantidade)
    
    # Marcar comanda para impressão
    if comanda.status == "impressa":
        comanda.status = "aberta"
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/comandas/{comanda_id}/itens/", response_model=List[schemas.ItemComanda])
def listar_itens_comanda(comanda_id: int, db: Session = Depends(get_db)):
    return db.query(models.ItemComanda).filter(models.ItemComanda.comanda_id == comanda_id).all()

@app.put("/itens/{item_id}/status")
def atualizar_status_item(item_id: int, status: str, db: Session = Depends(get_db)):
    item = db.query(models.ItemComanda).filter(models.ItemComanda.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    if status not in ["pendente", "preparando", "pronto"]:
        raise HTTPException(status_code=400, detail="Status inválido")
    
    item.status = status
    db.commit()
    return {"message": f"Status do item atualizado para {status}"}

# Endpoints para Garçons
@app.get("/garcons/", response_model=List[schemas.Garcom])
def listar_garcons(db: Session = Depends(get_db)):
    return db.query(models.Garcom).filter(models.Garcom.ativo == True).all()

@app.post("/garcons/", response_model=schemas.Garcom)
def criar_garcom(garcom: schemas.GarcomCreate, db: Session = Depends(get_db)):
    db_garcom = models.Garcom(**garcom.dict())
    db.add(db_garcom)
    db.commit()
    db.refresh(db_garcom)
    return db_garcom

@app.get("/garcons/{garcom_id}/atendimentos/", response_model=List[schemas.AtendimentoGarcom])
def listar_atendimentos_garcom(garcom_id: int, db: Session = Depends(get_db)):
    return db.query(models.AtendimentoGarcom).filter(
        models.AtendimentoGarcom.garcom_id == garcom_id
    ).all()

# Endpoint para chamar garçom
@app.post("/comandas/{comanda_id}/chamar-garcom")
def chamar_garcom(comanda_id: int, garcom_id: int = None, db: Session = Depends(get_db)):
    comanda = db.query(models.Comanda).filter(models.Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    
    # Marcar flag de chamada de garçom
    comanda.chamando_garcom = True
    db.commit()
    
    # Registrar atendimento do garçom
    if garcom_id:
        atendimento = models.AtendimentoGarcom(
            garcom_id=garcom_id,
            comanda_id=comanda_id,
            tipo="chamada"
        )
        db.add(atendimento)
        db.commit()
    
    return {"message": f"Garçom chamado para a mesa {comanda.mesa.numero}"}

@app.put("/comandas/{comanda_id}/atender-garcom")
def atender_garcom(comanda_id: int, db: Session = Depends(get_db)):
    comanda = db.query(models.Comanda).filter(models.Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    comanda.chamando_garcom = False
    db.commit()
    return {"message": f"Atendimento do garçom registrado para a mesa {comanda.mesa_id}"}

# Endpoints para Sincronização Offline
@app.post("/sincronizacao/")
def sincronizar_offline(sinc: schemas.SincronizacaoOfflineCreate, db: Session = Depends(get_db)):
    db_sinc = models.SincronizacaoOffline(**sinc.dict())
    db.add(db_sinc)
    db.commit()
    db.refresh(db_sinc)
    return {"message": "Sincronização registrada"}

@app.get("/sincronizacao/pendentes/", response_model=List[schemas.SincronizacaoOffline])
def listar_sincronizacoes_pendentes(db: Session = Depends(get_db)):
    return db.query(models.SincronizacaoOffline).filter(
        models.SincronizacaoOffline.sincronizado == False
    ).all()

@app.put("/sincronizacao/{sinc_id}/marcar-sincronizada")
def marcar_sincronizada(sinc_id: int, db: Session = Depends(get_db)):
    sinc = db.query(models.SincronizacaoOffline).filter(
        models.SincronizacaoOffline.id == sinc_id
    ).first()
    if not sinc:
        raise HTTPException(status_code=404, detail="Sincronização não encontrada")
    
    sinc.sincronizado = True
    sinc.data_sincronizacao = datetime.now()
    db.commit()
    return {"message": "Sincronização marcada como concluída"}

# Endpoint para obter categorias de produtos
@app.get("/produtos/categorias/")
def listar_categorias(db: Session = Depends(get_db)):
    categorias = db.query(models.Produto.categoria).distinct().all()
    return [cat[0] for cat in categorias]

# Endpoint para menu público (QR Code)
@app.get("/menu/{mesa_id}")
def obter_menu_publico(mesa_id: int, db: Session = Depends(get_db)):
    """Menu público acessível via QR Code"""
    mesa = db.query(models.Mesa).filter(models.Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa não encontrada")
    
    produtos = db.query(models.Produto).filter(models.Produto.disponivel == True).all()
    categorias = db.query(models.Produto.categoria).distinct().all()
    
    return {
        "mesa": {
            "id": mesa.id,
            "numero": mesa.numero
        },
        "categorias": [cat[0] for cat in categorias],
        "produtos": [
            {
                "id": p.id,
                "nome": p.nome,
                "preco": p.preco,
                "categoria": p.categoria,
                "descricao": p.descricao
            }
            for p in produtos
        ]
    }

# Endpoint para página principal
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Página principal do site da padaria"""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    index_path = os.path.join(static_dir, "index.html")
    
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    else:
        return HTMLResponse(content="""
        <html>
            <head><title>Padaria Delícias</title></head>
            <body>
                <h1>Bem-vindo à Padaria Delícias!</h1>
                <p>Site em construção. Em breve estará disponível.</p>
            </body>
        </html>
        """)

# Endpoints para Pedidos Online
@app.post("/pedidos-online/", response_model=schemas.PedidoOnline)
async def criar_pedido_online(pedido: schemas.PedidoOnlineCreate, db: Session = Depends(get_db)):
    """Criar pedido online para entrega"""
    try:
        # Calcular total do pedido
        total = 0
        for item in pedido.itens:
            produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
            if not produto:
                raise HTTPException(status_code=404, detail=f"Produto {item.produto_id} não encontrado")
            if not produto.disponivel:
                raise HTTPException(status_code=400, detail=f"Produto {produto.nome} não disponível")

            total += produto.preco * item.quantidade
        
        # Criar pedido
        db_pedido = models.PedidoOnline(
            nome_cliente=pedido.nome_cliente,
            telefone=pedido.telefone,
            endereco=pedido.endereco,
            forma_pagamento=pedido.forma_pagamento,
            observacoes=pedido.observacoes,
            total=total
        )
        db.add(db_pedido)
        db.commit()
        db.refresh(db_pedido)
        
        # Criar itens do pedido e decrementar estoque
        for item in pedido.itens:
            produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
            db_item = models.ItemPedidoOnline(
                pedido_id=db_pedido.id,
                produto_id=item.produto_id,
                quantidade=item.quantidade,
                preco_unitario=produto.preco,
                observacoes=item.observacoes
            )
            db.add(db_item)

        
        db.commit()
        
        # Preparar dados para WhatsApp
        pedido_data = {
            "id": db_pedido.id,
            "nome_cliente": db_pedido.nome_cliente,
            "telefone": db_pedido.telefone,
            "endereco": db_pedido.endereco,
            "forma_pagamento": db_pedido.forma_pagamento,
            "total": db_pedido.total,
            "observacoes": db_pedido.observacoes,
            "itens": []
        }
        
        # Adicionar itens ao pedido_data
        for item in pedido.itens:
            produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
            pedido_data["itens"].append({
                "quantidade": item.quantidade,
                "preco_unitario": produto.preco,
                "produto": {
                    "nome": produto.nome
                }
            })
        
        # Enviar para WhatsApp
        from .config_whatsapp import whatsapp_service
        whatsapp_service.enviar_pedido_whatsapp(pedido_data)
        
        # Marcar como enviado
        db_pedido.whatsapp_enviado = True
        db.commit()
        
        return db_pedido
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao processar pedido: {str(e)}")

@app.get("/pedidos-online/", response_model=List[schemas.PedidoOnlineResumo])
def listar_pedidos_online(db: Session = Depends(get_db)):
    """Listar todos os pedidos online"""
    pedidos = db.query(models.PedidoOnline).order_by(models.PedidoOnline.data_pedido.desc()).all()
    resultado = []
    for pedido in pedidos:
        resultado.append(schemas.PedidoOnlineResumo(
            id=pedido.id,
            nome_cliente=pedido.nome_cliente,
            telefone=pedido.telefone,
            total=pedido.total,
            status=pedido.status,
            data_pedido=pedido.data_pedido,
            quantidade_itens=len(pedido.itens)
        ))
    return resultado

@app.get("/pedidos-online/{pedido_id}", response_model=schemas.PedidoOnline)
def obter_pedido_online(pedido_id: int, db: Session = Depends(get_db)):
    """Obter detalhes de um pedido online"""
    pedido = db.query(models.PedidoOnline).filter(models.PedidoOnline.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@app.put("/pedidos-online/{pedido_id}/status")
def atualizar_status_pedido(pedido_id: int, status: str, db: Session = Depends(get_db)):
    """Atualizar status de um pedido online"""
    pedido = db.query(models.PedidoOnline).filter(models.PedidoOnline.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    status_validos = ["pendente", "confirmado", "preparando", "entregando", "entregue", "cancelado"]
    if status not in status_validos:
        raise HTTPException(status_code=400, detail="Status inválido")
    
    pedido.status = status
    
    # Atualizar timestamps
    if status == "confirmado" and not pedido.data_confirmacao:
        pedido.data_confirmacao = datetime.now()
    elif status == "entregue" and not pedido.data_entrega:
        pedido.data_entrega = datetime.now()
    
    db.commit()
    return {"message": f"Status do pedido atualizado para {status}"}

# Endpoint para contato
@app.post("/contato/")
async def enviar_contato(contato: dict):
    """Enviar mensagem de contato"""
    try:
        # Aqui você pode implementar a lógica para enviar email ou salvar contato
        return {
            "success": True,
            "message": "Mensagem enviada com sucesso! Entraremos em contato em breve."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar mensagem: {str(e)}")

@app.get("/comandas/{comanda_id}/status")
def status_comanda(comanda_id: int, db: Session = Depends(get_db)):
    comanda = db.query(models.Comanda).filter(models.Comanda.id == comanda_id).first()
    if not comanda:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    itens = db.query(models.ItemComanda).filter(models.ItemComanda.comanda_id == comanda_id).all()
    status_itens = [item.status for item in itens]
    # Lógica para status geral dos itens
    if all(s == "pronto" for s in status_itens) and status_itens:
        status_geral = "pronto"
    elif any(s == "preparando" for s in status_itens):
        status_geral = "preparando"
    elif all(s == "pendente" for s in status_itens):
        status_geral = "pendente"
    else:
        status_geral = "parcial"
    return {
        "comanda_id": comanda.id,
        "mesa_numero": comanda.mesa.numero if comanda.mesa else None,
        "status_comanda": comanda.status,
        "status_geral_itens": status_geral,
        "itens": [
            {"produto": item.produto.nome if item.produto else "", "status": item.status}
            for item in itens
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 