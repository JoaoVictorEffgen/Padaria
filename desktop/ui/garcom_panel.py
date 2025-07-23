from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QGroupBox,
                             QComboBox, QHeaderView, QMessageBox, QDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtMultimedia import QSound
from ..services.api_client import APIClient

class GarcomPanel(QWidget):
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.chamada_alerta_widget = None
        self.chamada_alerta_sound = None
        self.chamada_comanda_id = None
        self.init_ui()
        self.setup_timer()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Painel do Garçom")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Filtros
        filter_layout = QHBoxLayout()
        
        # Filtro por status
        filter_layout.addWidget(QLabel("Filtrar por:"))
        self.combo_filter = QComboBox()
        self.combo_filter.addItems(["Todas", "Abertas", "Para Impressão", "Aguardando Pagamento"])
        self.combo_filter.currentTextChanged.connect(self.atualizar_comandas)
        filter_layout.addWidget(self.combo_filter)
        
        # Botão atualizar
        btn_atualizar = QPushButton("Atualizar")
        btn_atualizar.clicked.connect(self.atualizar_comandas)
        filter_layout.addWidget(btn_atualizar)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Tabela de comandas
        self.table_comandas = QTableWidget()
        self.table_comandas.setColumnCount(8)
        self.table_comandas.setHorizontalHeaderLabels([
            "Mesa", "Status", "Total", "Itens", "Tempo", "Observações", "Ações", "Detalhes"
        ])
        
        # Configurar tabela
        header = self.table_comandas.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Mesa
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Total
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Itens
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Tempo
        header.setSectionResizeMode(5, QHeaderView.Stretch)           # Observações
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Ações
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Detalhes
        
        layout.addWidget(self.table_comandas)
        
        # Estatísticas
        stats_group = QGroupBox("Estatísticas")
        stats_layout = QHBoxLayout(stats_group)
        
        self.lbl_total_comandas = QLabel("Total: 0")
        self.lbl_comandas_abertas = QLabel("Abertas: 0")
        self.lbl_comandas_impressao = QLabel("Para Impressão: 0")
        self.lbl_comandas_pagamento = QLabel("Aguardando Pagamento: 0")
        
        stats_layout.addWidget(self.lbl_total_comandas)
        stats_layout.addWidget(self.lbl_comandas_abertas)
        stats_layout.addWidget(self.lbl_comandas_impressao)
        stats_layout.addWidget(self.lbl_comandas_pagamento)
        stats_layout.addStretch()
        
        layout.addWidget(stats_group)
        
    def setup_timer(self):
        """Configura timer para atualização automática"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_comandas)
        self.timer.start(10000)  # Atualiza a cada 10 segundos
        
    def atualizar_comandas(self):
        """Atualiza a lista de comandas e exibe alerta de chamada de garçom se necessário"""
        try:
            comandas = self.api_client.listar_comandas()
            
            # Filtrar comandas
            filtro = self.combo_filter.currentText()
            if filtro == "Abertas":
                comandas = [c for c in comandas if c["status"] == "aberta"]
            elif filtro == "Para Impressão":
                comandas = [c for c in comandas if c["status"] in ["aberta", "impressa"]]
            elif filtro == "Aguardando Pagamento":
                comandas = [c for c in comandas if c["status"] == "aguardando_pagamento"]
            
            # Verificar se há chamada de garçom
            chamada = next((c for c in comandas if c.get("chamando_garcom")), None)
            if chamada:
                self.exibir_alerta_chamada(chamada)
            else:
                self.ocultar_alerta_chamada()
            
            self.table_comandas.setRowCount(len(comandas))
            
            # Contadores para estatísticas
            total = len(comandas)
            abertas = len([c for c in comandas if c["status"] == "aberta"])
            impressao = len([c for c in comandas if c["status"] in ["aberta", "impressa"]])
            pagamento = len([c for c in comandas if c["status"] == "aguardando_pagamento"])
            
            for i, comanda in enumerate(comandas):
                # Mesa
                self.table_comandas.setItem(i, 0, QTableWidgetItem(f"Mesa {comanda['mesa_numero']}"))
                
                # Status com cores
                status_item = QTableWidgetItem(comanda["status"].replace("_", " ").title())
                if comanda["status"] == "aberta":
                    status_item.setBackground(QColor(255, 255, 200))  # Amarelo claro
                elif comanda["status"] == "aguardando_pagamento":
                    status_item.setBackground(QColor(255, 200, 200))  # Vermelho claro
                elif comanda["status"] == "impressa":
                    status_item.setBackground(QColor(200, 255, 200))  # Verde claro
                self.table_comandas.setItem(i, 1, status_item)
                
                # Total
                self.table_comandas.setItem(i, 2, QTableWidgetItem(f"R$ {comanda['total']:.2f}"))
                
                # Itens
                self.table_comandas.setItem(i, 3, QTableWidgetItem(str(comanda["quantidade_itens"])))
                
                # Tempo (simulado - você pode implementar cálculo real)
                tempo = "5 min"  # Placeholder
                self.table_comandas.setItem(i, 4, QTableWidgetItem(tempo))
                
                # Observações (placeholder)
                obs = "Sem observações"
                self.table_comandas.setItem(i, 5, QTableWidgetItem(obs))
                
                # Ações
                btn_layout = QHBoxLayout()
                
                if comanda["status"] == "aberta":
                    btn_imprimir = QPushButton("Imprimir")
                    btn_imprimir.clicked.connect(lambda checked, c=comanda: self.imprimir_comanda(c))
                    btn_layout.addWidget(btn_imprimir)
                    
                    btn_entregar = QPushButton("Entregar")
                    btn_entregar.clicked.connect(lambda checked, c=comanda: self.entregar_comanda(c))
                    btn_layout.addWidget(btn_entregar)
                
                elif comanda["status"] == "aguardando_pagamento":
                    btn_finalizar = QPushButton("Finalizar")
                    btn_finalizar.clicked.connect(lambda checked, c=comanda: self.finalizar_comanda(c))
                    btn_layout.addWidget(btn_finalizar)
                
                # Widget para as ações
                actions_widget = QWidget()
                actions_widget.setLayout(btn_layout)
                self.table_comandas.setCellWidget(i, 6, actions_widget)
                
                # Botão detalhes
                btn_detalhes = QPushButton("Ver Detalhes")
                btn_detalhes.clicked.connect(lambda checked, c=comanda: self.ver_detalhes(c))
                self.table_comandas.setCellWidget(i, 7, btn_detalhes)
            
            # Atualizar estatísticas
            self.lbl_total_comandas.setText(f"Total: {total}")
            self.lbl_comandas_abertas.setText(f"Abertas: {abertas}")
            self.lbl_comandas_impressao.setText(f"Para Impressão: {impressao}")
            self.lbl_comandas_pagamento.setText(f"Aguardando Pagamento: {pagamento}")
            
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar comandas: {e}")
    
    def imprimir_comanda(self, comanda):
        """Marca comanda como impressa"""
        try:
            self.api_client.marcar_comanda_impressa(comanda["id"])
            QMessageBox.information(self, "Sucesso", f"Comanda da Mesa {comanda['mesa_numero']} marcada como impressa")
            self.atualizar_comandas()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao imprimir comanda: {e}")
    
    def entregar_comanda(self, comanda):
        """Marca comanda como entregue"""
        try:
            # Aqui você pode implementar a lógica de entrega
            QMessageBox.information(self, "Sucesso", f"Comanda da Mesa {comanda['mesa_numero']} marcada como entregue")
            self.atualizar_comandas()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao entregar comanda: {e}")
    
    def finalizar_comanda(self, comanda):
        """Finaliza o pagamento da comanda"""
        try:
            self.api_client.finalizar_comanda(comanda["id"])
            QMessageBox.information(self, "Sucesso", f"Pagamento da Mesa {comanda['mesa_numero']} finalizado")
            self.atualizar_comandas()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao finalizar comanda: {e}")
    
    def ver_detalhes(self, comanda):
        """Mostra detalhes da comanda"""
        try:
            detalhes = self.api_client.obter_comanda(comanda["id"])
            
            # Criar mensagem com detalhes
            msg = f"Comanda #{detalhes['id']} - Mesa {detalhes['mesa']['numero']}\n"
            msg += f"Status: {detalhes['status']}\n"
            msg += f"Total: R$ {detalhes['total']:.2f}\n"
            msg += f"Data: {detalhes['data_abertura']}\n\n"
            msg += "Itens:\n"
            
            for item in detalhes['itens']:
                msg += f"• {item['produto']['nome']} x{item['quantidade']} - R$ {item['subtotal']:.2f}\n"
                if item.get('observacoes'):
                    msg += f"  Obs: {item['observacoes']}\n"
            
            if detalhes.get('observacoes'):
                msg += f"\nObservações: {detalhes['observacoes']}"
            
            QMessageBox.information(self, "Detalhes da Comanda", msg)
            
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar detalhes: {e}") 

    def exibir_alerta_chamada(self, comanda):
        """Exibe alerta visual e sonoro de chamada de garçom"""
        if self.chamada_alerta_widget:
            # Já está exibindo
            return
        self.chamada_comanda_id = comanda["id"]
        self.chamada_alerta_widget = QDialog(self)
        self.chamada_alerta_widget.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.chamada_alerta_widget.setModal(False)
        palette = self.chamada_alerta_widget.palette()
        palette.setColor(QPalette.Window, QColor("#ff4444"))
        self.chamada_alerta_widget.setPalette(palette)
        self.chamada_alerta_widget.setAutoFillBackground(True)
        layout = QVBoxLayout()
        label = QLabel(f"MESA {comanda['mesa_numero']} CHAMANDO GARÇOM!")
        label.setFont(QFont("Arial", 36, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        btn_atender = QPushButton("Atender chamada")
        btn_atender.setFont(QFont("Arial", 20, QFont.Bold))
        btn_atender.clicked.connect(self.atender_chamada_garcom)
        layout.addWidget(btn_atender)
        self.chamada_alerta_widget.setLayout(layout)
        self.chamada_alerta_widget.resize(600, 200)
        self.chamada_alerta_widget.show()
        # Som de alerta
        self.chamada_alerta_sound = QSound("alerta.wav")
        self.chamada_alerta_sound.setLoops(QSound.Infinite)
        self.chamada_alerta_sound.play()
    def ocultar_alerta_chamada(self):
        if self.chamada_alerta_widget:
            self.chamada_alerta_widget.close()
            self.chamada_alerta_widget = None
        if self.chamada_alerta_sound:
            self.chamada_alerta_sound.stop()
            self.chamada_alerta_sound = None
        self.chamada_comanda_id = None
    def atender_chamada_garcom(self):
        """Envia requisição para atender chamada de garçom e oculta alerta"""
        if self.chamada_comanda_id:
            try:
                self.api_client._make_request("PUT", f"/comandas/{self.chamada_comanda_id}/atender-garcom")
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao atender chamada: {e}")
        self.ocultar_alerta_chamada()
        self.atualizar_comandas() 