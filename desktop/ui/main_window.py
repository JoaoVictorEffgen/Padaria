from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QTableWidget, QTableWidgetItem, QPushButton,
                             QLabel, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox,
                             QTextEdit, QMessageBox, QGroupBox, QGridLayout, QSplitter,
                             QDialog, QFormLayout, QHeaderView, QScrollArea, QFileDialog)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QIcon
from ..services.api_client import APIClient
import json
from datetime import datetime, date
import csv
import os
from .charts_widget import ChartsWidget

class AdicionarProdutoDialog(QDialog):
    """Diálogo para adicionar produto à comanda"""
    def __init__(self, produtos, parent=None):
        super().__init__(parent)
        self.produtos = produtos
        self.produto_selecionado = None
        self.quantidade = 1
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Adicionar Produto à Comanda")
        self.setModal(True)
        self.setFixedSize(300, 150)
        
        layout = QFormLayout(self)
        
        # Combo de produtos
        self.combo_produtos = QComboBox()
        for produto in self.produtos:
            self.combo_produtos.addItem(f"{produto['nome']} - R$ {produto['preco']:.2f}", produto)
        layout.addRow("Produto:", self.combo_produtos)
        
        # Spin de quantidade
        self.spin_quantidade = QSpinBox()
        self.spin_quantidade.setMinimum(1)
        self.spin_quantidade.setMaximum(99)
        self.spin_quantidade.setValue(1)
        layout.addRow("Quantidade:", self.spin_quantidade)
        
        # Botões
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("Adicionar")
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addRow(btn_layout)
        
    def get_produto_quantidade(self):
        """Retorna o produto e quantidade selecionados"""
        if self.result() == QDialog.Accepted:
            produto = self.combo_produtos.currentData()
            quantidade = self.spin_quantidade.value()
            return produto, quantidade
        return None, 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.comanda_atual = None
        self.pedido_online_atual = None
        self.ultima_data = None
        self.init_ui()
        self.setup_timer()
        # Verificar se é um novo dia e limpar se necessário
        self.verificar_novo_dia()
        # Carregar dados iniciais
        self.atualizar_dados()
        
    def init_ui(self):
        self.setWindowTitle("Sistema Padaria - Desktop")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        
        # Título
        title = QLabel("Sistema de Gerenciamento - Padaria")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Tabs
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Criar abas
        self.create_comandas_tab()
        self.create_produtos_tab()
        self.create_mesas_tab()
        self.create_pedidos_online_tab()
        self.create_relatorios_tab()
        
    def create_comandas_tab(self):
        """Cria a aba de comandas"""
        comandas_widget = QWidget()
        layout = QHBoxLayout(comandas_widget)
        
        # Painel esquerdo - Lista de comandas
        left_panel = QGroupBox("Comandas Ativas")
        left_layout = QVBoxLayout(left_panel)
        
        # Botões de ação
        btn_layout = QHBoxLayout()
        self.btn_nova_comanda = QPushButton("Nova Comanda")
        self.btn_nova_comanda.clicked.connect(self.nova_comanda)
        self.btn_atualizar = QPushButton("Atualizar")
        self.btn_atualizar.clicked.connect(self.atualizar_comandas)
        
        btn_layout.addWidget(self.btn_nova_comanda)
        btn_layout.addWidget(self.btn_atualizar)
        left_layout.addLayout(btn_layout)
        
        # Tabela de comandas
        self.table_comandas = QTableWidget()
        self.table_comandas.setColumnCount(6)
        self.table_comandas.setHorizontalHeaderLabels([
            "ID", "Mesa", "Status", "Total", "Itens", "Ações"
        ])
        self.table_comandas.itemSelectionChanged.connect(self.selecionar_comanda)
        left_layout.addWidget(self.table_comandas)
        
        # Painel direito - Detalhes da comanda
        right_panel = QGroupBox("Detalhes da Comanda")
        right_layout = QVBoxLayout(right_panel)
        
        # Informações da comanda
        info_layout = QGridLayout()
        info_layout.addWidget(QLabel("Mesa:"), 0, 0)
        self.lbl_mesa = QLabel("-")
        info_layout.addWidget(self.lbl_mesa, 0, 1)
        
        info_layout.addWidget(QLabel("Status:"), 1, 0)
        self.lbl_status = QLabel("-")
        info_layout.addWidget(self.lbl_status, 1, 1)
        
        info_layout.addWidget(QLabel("Total:"), 2, 0)
        self.lbl_total = QLabel("R$ 0,00")
        self.lbl_total.setFont(QFont("Arial", 14, QFont.Bold))
        info_layout.addWidget(self.lbl_total, 2, 1)
        
        right_layout.addLayout(info_layout)
        
        # Tabela de itens
        self.table_itens = QTableWidget()
        self.table_itens.setColumnCount(4)
        self.table_itens.setHorizontalHeaderLabels([
            "Produto", "Quantidade", "Preço Unit.", "Subtotal"
        ])
        right_layout.addWidget(self.table_itens)
        
        # Botões de ação da comanda
        btn_comanda_layout = QHBoxLayout()
        self.btn_adicionar_produto = QPushButton("Adicionar Produto")
        self.btn_adicionar_produto.clicked.connect(self.adicionar_produto_comanda)
        self.btn_fechar_comanda = QPushButton("Fechar Comanda")
        self.btn_fechar_comanda.clicked.connect(self.fechar_comanda)
        self.btn_finalizar_comanda = QPushButton("Finalizar Pagamento")
        self.btn_finalizar_comanda.clicked.connect(self.finalizar_comanda)
        self.btn_cancelar_comanda = QPushButton("Cancelar Comanda")
        self.btn_cancelar_comanda.clicked.connect(self.cancelar_comanda)
        
        btn_comanda_layout.addWidget(self.btn_adicionar_produto)
        btn_comanda_layout.addWidget(self.btn_fechar_comanda)
        btn_comanda_layout.addWidget(self.btn_finalizar_comanda)
        btn_comanda_layout.addWidget(self.btn_cancelar_comanda)
        right_layout.addLayout(btn_comanda_layout)
        
        # Adicionar painéis ao layout principal
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 800])
        layout.addWidget(splitter)
        
        self.tab_widget.addTab(comandas_widget, "Comandas")
        
    def create_produtos_tab(self):
        """Cria a aba de produtos"""
        produtos_widget = QWidget()
        layout = QVBoxLayout(produtos_widget)
        
        # Formulário de cadastro
        form_group = QGroupBox("Cadastrar Produto")
        form_layout = QGridLayout(form_group)
        
        form_layout.addWidget(QLabel("Nome:"), 0, 0)
        self.txt_nome_produto = QLineEdit()
        form_layout.addWidget(self.txt_nome_produto, 0, 1)
        
        form_layout.addWidget(QLabel("Preço:"), 1, 0)
        self.spin_preco = QDoubleSpinBox()
        self.spin_preco.setMaximum(999.99)
        self.spin_preco.setDecimals(2)
        self.spin_preco.setPrefix("R$ ")
        form_layout.addWidget(self.spin_preco, 1, 1)
        
        form_layout.addWidget(QLabel("Categoria:"), 2, 0)
        self.combo_categoria = QComboBox()
        self.combo_categoria.setEditable(True)
        self.combo_categoria.addItems(["Pães", "Bebidas", "Doces", "Salgados", "Cafés"])
        form_layout.addWidget(self.combo_categoria, 2, 1)
        
        form_layout.addWidget(QLabel("Descrição:"), 3, 0)
        self.txt_descricao = QTextEdit()
        self.txt_descricao.setMaximumHeight(60)
        form_layout.addWidget(self.txt_descricao, 3, 1)
        
        btn_cadastrar = QPushButton("Cadastrar Produto")
        btn_cadastrar.clicked.connect(self.cadastrar_produto)
        form_layout.addWidget(btn_cadastrar, 4, 0, 1, 2)
        
        layout.addWidget(form_group)
        
        # Tabela de produtos
        self.table_produtos = QTableWidget()
        self.table_produtos.setColumnCount(5)
        self.table_produtos.setHorizontalHeaderLabels([
            "ID", "Nome", "Preço", "Categoria", "Descrição"
        ])
        layout.addWidget(self.table_produtos)
        
        self.tab_widget.addTab(produtos_widget, "Produtos")
        
    def create_mesas_tab(self):
        """Cria a aba de mesas"""
        mesas_widget = QWidget()
        layout = QVBoxLayout(mesas_widget)
        
        # Formulário de mesa
        form_group = QGroupBox("Cadastrar Mesa")
        form_layout = QHBoxLayout(form_group)
        
        form_layout.addWidget(QLabel("Número da Mesa:"))
        self.spin_numero_mesa = QSpinBox()
        self.spin_numero_mesa.setMaximum(999)
        form_layout.addWidget(self.spin_numero_mesa)
        
        btn_cadastrar_mesa = QPushButton("Cadastrar Mesa")
        btn_cadastrar_mesa.clicked.connect(self.cadastrar_mesa)
        form_layout.addWidget(btn_cadastrar_mesa)
        
        layout.addWidget(form_group)
        
        # Tabela de mesas
        self.table_mesas = QTableWidget()
        self.table_mesas.setColumnCount(4)
        self.table_mesas.setHorizontalHeaderLabels([
            "ID", "Número", "Status", "Ações"
        ])
        layout.addWidget(self.table_mesas)
        
        self.tab_widget.addTab(mesas_widget, "Mesas")
        
    def create_pedidos_online_tab(self):
        """Cria a aba de pedidos online"""
        pedidos_widget = QWidget()
        layout = QHBoxLayout(pedidos_widget)
        
        # Painel esquerdo - Lista de pedidos
        left_panel = QGroupBox("Pedidos Online")
        left_layout = QVBoxLayout(left_panel)
        
        # Botões de ação
        btn_layout = QHBoxLayout()
        self.btn_atualizar_pedidos = QPushButton("Atualizar")
        self.btn_atualizar_pedidos.clicked.connect(self.atualizar_pedidos_online)
        
        btn_layout.addWidget(self.btn_atualizar_pedidos)
        left_layout.addLayout(btn_layout)
        
        # Tabela de pedidos
        self.table_pedidos_online = QTableWidget()
        self.table_pedidos_online.setColumnCount(7)
        self.table_pedidos_online.setHorizontalHeaderLabels([
            "ID", "Cliente", "Telefone", "Total", "Status", "Data", "Ações"
        ])
        self.table_pedidos_online.itemSelectionChanged.connect(self.selecionar_pedido_online)
        left_layout.addWidget(self.table_pedidos_online)
        
        # Painel direito - Detalhes do pedido
        right_panel = QGroupBox("Detalhes do Pedido")
        right_layout = QVBoxLayout(right_panel)
        
        # Informações do pedido
        info_layout = QGridLayout()
        info_layout.addWidget(QLabel("Cliente:"), 0, 0)
        self.lbl_cliente = QLabel("-")
        info_layout.addWidget(self.lbl_cliente, 0, 1)
        
        info_layout.addWidget(QLabel("Telefone:"), 1, 0)
        self.lbl_telefone = QLabel("-")
        info_layout.addWidget(self.lbl_telefone, 1, 1)
        
        info_layout.addWidget(QLabel("Endereço:"), 2, 0)
        self.lbl_endereco = QLabel("-")
        info_layout.addWidget(self.lbl_endereco, 2, 1)
        
        info_layout.addWidget(QLabel("Pagamento:"), 3, 0)
        self.lbl_pagamento = QLabel("-")
        info_layout.addWidget(self.lbl_pagamento, 3, 1)
        
        info_layout.addWidget(QLabel("Status:"), 4, 0)
        self.lbl_status_pedido = QLabel("-")
        info_layout.addWidget(self.lbl_status_pedido, 4, 1)
        
        info_layout.addWidget(QLabel("Total:"), 5, 0)
        self.lbl_total_pedido = QLabel("R$ 0,00")
        self.lbl_total_pedido.setFont(QFont("Arial", 14, QFont.Bold))
        info_layout.addWidget(self.lbl_total_pedido, 5, 1)
        
        right_layout.addLayout(info_layout)
        
        # Observações
        right_layout.addWidget(QLabel("Observações:"))
        self.txt_observacoes_pedido = QTextEdit()
        self.txt_observacoes_pedido.setMaximumHeight(80)
        self.txt_observacoes_pedido.setReadOnly(True)
        right_layout.addWidget(self.txt_observacoes_pedido)
        
        # Tabela de itens
        right_layout.addWidget(QLabel("Itens do Pedido:"))
        self.table_itens_pedido = QTableWidget()
        self.table_itens_pedido.setColumnCount(4)
        self.table_itens_pedido.setHorizontalHeaderLabels([
            "Produto", "Quantidade", "Preço Unit.", "Subtotal"
        ])
        right_layout.addWidget(self.table_itens_pedido)
        
        # Botões de ação do pedido
        btn_pedido_layout = QHBoxLayout()
        self.btn_confirmar_pedido = QPushButton("Confirmar Pedido")
        self.btn_confirmar_pedido.clicked.connect(self.confirmar_pedido)
        self.btn_preparando_pedido = QPushButton("Em Preparação")
        self.btn_preparando_pedido.clicked.connect(self.preparando_pedido)
        self.btn_entregando_pedido = QPushButton("Entregando")
        self.btn_entregando_pedido.clicked.connect(self.entregando_pedido)
        self.btn_entregue_pedido = QPushButton("Entregue")
        self.btn_entregue_pedido.clicked.connect(self.entregue_pedido)
        self.btn_cancelar_pedido = QPushButton("Cancelar Pedido")
        self.btn_cancelar_pedido.clicked.connect(self.cancelar_pedido_online)
        
        btn_pedido_layout.addWidget(self.btn_confirmar_pedido)
        btn_pedido_layout.addWidget(self.btn_preparando_pedido)
        btn_pedido_layout.addWidget(self.btn_entregando_pedido)
        btn_pedido_layout.addWidget(self.btn_entregue_pedido)
        btn_pedido_layout.addWidget(self.btn_cancelar_pedido)
        right_layout.addLayout(btn_pedido_layout)
        
        # Adicionar painéis ao layout principal
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 800])
        layout.addWidget(splitter)
        
        self.tab_widget.addTab(pedidos_widget, "Pedidos Online")
        
    def create_relatorios_tab(self):
        """Cria a aba de relatórios"""
        relatorios_widget = QWidget()
        layout = QVBoxLayout(relatorios_widget)
        
        # Botões de ação
        btn_layout = QHBoxLayout()
        self.btn_limpar_telas = QPushButton("Limpar Todas as Telas")
        self.btn_limpar_telas.clicked.connect(self.limpar_todas_telas)
        self.btn_download_relatorio = QPushButton("Baixar Relatório")
        self.btn_download_relatorio.clicked.connect(self.baixar_relatorio)
        
        btn_layout.addWidget(self.btn_limpar_telas)
        btn_layout.addWidget(self.btn_download_relatorio)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Estatísticas
        stats_group = QGroupBox("Estatísticas")
        stats_layout = QGridLayout(stats_group)
        
        self.lbl_total_comandas = QLabel("0")
        self.lbl_comandas_abertas = QLabel("0")
        self.lbl_comandas_fechadas = QLabel("0")
        self.lbl_faturamento_dia = QLabel("R$ 0,00")
        
        stats_layout.addWidget(QLabel("Total de Comandas:"), 0, 0)
        stats_layout.addWidget(self.lbl_total_comandas, 0, 1)
        stats_layout.addWidget(QLabel("Comandas Abertas:"), 1, 0)
        stats_layout.addWidget(self.lbl_comandas_abertas, 1, 1)
        stats_layout.addWidget(QLabel("Comandas Fechadas:"), 2, 0)
        stats_layout.addWidget(self.lbl_comandas_fechadas, 2, 1)
        stats_layout.addWidget(QLabel("Faturamento do Dia:"), 3, 0)
        stats_layout.addWidget(self.lbl_faturamento_dia, 3, 1)
        
        layout.addWidget(stats_group)
        
        # Gráficos
        self.charts_widget = ChartsWidget(self.api_client)
        layout.addWidget(self.charts_widget)
        
        # Histórico de comandas
        historico_group = QGroupBox("Histórico de Comandas")
        historico_layout = QVBoxLayout(historico_group)
        
        self.table_historico = QTableWidget()
        self.table_historico.setColumnCount(6)
        self.table_historico.setHorizontalHeaderLabels([
            "ID", "Mesa", "Status", "Total", "Data Abertura", "Data Fechamento"
        ])
        historico_layout.addWidget(self.table_historico)
        
        layout.addWidget(historico_group)
        
        self.tab_widget.addTab(relatorios_widget, "Relatórios")
        
    def setup_timer(self):
        """Configura timer para atualização automática"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_dados)
        self.timer.start(30000)  # Atualizar a cada 30 segundos
        
    def atualizar_dados(self):
        """Atualiza todos os dados"""
        self.atualizar_comandas()
        self.atualizar_produtos()
        self.atualizar_mesas()
        self.atualizar_pedidos_online()
        self.atualizar_relatorios()
        
    def atualizar_comandas(self):
        """Atualiza a lista de comandas"""
        try:
            comandas = self.api_client.listar_comandas()
            
            self.table_comandas.setRowCount(len(comandas))
            for i, comanda in enumerate(comandas):
                self.table_comandas.setItem(i, 0, QTableWidgetItem(str(comanda["id"])))
                self.table_comandas.setItem(i, 1, QTableWidgetItem(str(comanda["mesa_numero"])))
                self.table_comandas.setItem(i, 2, QTableWidgetItem(comanda["status"]))
                self.table_comandas.setItem(i, 3, QTableWidgetItem(f"R$ {comanda['total']:.2f}"))
                self.table_comandas.setItem(i, 4, QTableWidgetItem(str(comanda["quantidade_itens"])))
                
                # Botão para ver detalhes
                btn_ver = QPushButton("Ver")
                btn_ver.clicked.connect(lambda checked, c=comanda: self.ver_comanda(c))
                self.table_comandas.setCellWidget(i, 5, btn_ver)
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar comandas: {e}")
            
    def atualizar_produtos(self):
        """Atualiza a lista de produtos"""
        try:
            produtos = self.api_client.listar_produtos()
            
            self.table_produtos.setRowCount(len(produtos))
            for i, produto in enumerate(produtos):
                self.table_produtos.setItem(i, 0, QTableWidgetItem(str(produto["id"])))
                self.table_produtos.setItem(i, 1, QTableWidgetItem(produto["nome"]))
                self.table_produtos.setItem(i, 2, QTableWidgetItem(f"R$ {produto['preco']:.2f}"))
                self.table_produtos.setItem(i, 3, QTableWidgetItem(produto["categoria"]))
                self.table_produtos.setItem(i, 4, QTableWidgetItem(produto.get("descricao", "")))
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar produtos: {e}")
            
    def atualizar_mesas(self):
        """Atualiza a lista de mesas"""
        try:
            mesas = self.api_client.listar_mesas()
            
            self.table_mesas.setRowCount(len(mesas))
            for i, mesa in enumerate(mesas):
                self.table_mesas.setItem(i, 0, QTableWidgetItem(str(mesa["id"])))
                self.table_mesas.setItem(i, 1, QTableWidgetItem(str(mesa["numero"])))
                self.table_mesas.setItem(i, 2, QTableWidgetItem(mesa["status"]))
                
                # Botão para abrir comanda
                btn_abrir = QPushButton("Abrir Comanda")
                btn_abrir.clicked.connect(lambda checked, m=mesa: self.abrir_comanda_mesa(m))
                self.table_mesas.setCellWidget(i, 3, btn_abrir)
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar mesas: {e}")
            
    def atualizar_pedidos_online(self):
        """Atualiza a lista de pedidos online"""
        try:
            pedidos = self.api_client.listar_pedidos_online()
            
            self.table_pedidos_online.setRowCount(len(pedidos))
            for i, pedido in enumerate(pedidos):
                self.table_pedidos_online.setItem(i, 0, QTableWidgetItem(str(pedido["id"])))
                self.table_pedidos_online.setItem(i, 1, QTableWidgetItem(pedido["nome_cliente"]))
                self.table_pedidos_online.setItem(i, 2, QTableWidgetItem(pedido["telefone"]))
                self.table_pedidos_online.setItem(i, 3, QTableWidgetItem(f"R$ {pedido['total']:.2f}"))
                self.table_pedidos_online.setItem(i, 4, QTableWidgetItem(pedido["status"]))
                self.table_pedidos_online.setItem(i, 5, QTableWidgetItem(str(pedido["data_pedido"])))
                
                # Botão para ver detalhes
                btn_ver = QPushButton("Ver")
                btn_ver.clicked.connect(lambda checked, p=pedido: self.ver_pedido_online(p))
                self.table_pedidos_online.setCellWidget(i, 6, btn_ver)
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar pedidos online: {e}")
            
    def atualizar_relatorios(self):
        """Atualiza os relatórios"""
        try:
            comandas = self.api_client.listar_comandas()
            
            total = len(comandas)
            abertas = len([c for c in comandas if c["status"] == "aberta"])
            fechadas = len([c for c in comandas if c["status"] == "fechada"])
            faturamento = sum([c["total"] for c in comandas if c["status"] == "fechada"])
            
            self.lbl_total_comandas.setText(str(total))
            self.lbl_comandas_abertas.setText(str(abertas))
            self.lbl_comandas_fechadas.setText(str(fechadas))
            self.lbl_faturamento_dia.setText(f"R$ {faturamento:.2f}")
            
            # Atualizar gráficos
            if hasattr(self, 'charts_widget'):
                self.charts_widget.atualizar_graficos()
            
            # Histórico - mostrar apenas comandas do dia
            from datetime import datetime
            hoje = datetime.now().date()
            comandas_do_dia = []
            for c in comandas:
                data_abertura = c["data_abertura"]
                if isinstance(data_abertura, str):
                    if 'T' in data_abertura:
                        data = datetime.fromisoformat(data_abertura.replace('Z', '+00:00')).date()
                    else:
                        data = datetime.strptime(data_abertura, '%Y-%m-%d').date()
                else:
                    data = data_abertura.date()
                if data == hoje:
                    comandas_do_dia.append(c)
            self.table_historico.setRowCount(len(comandas_do_dia))
            for i, comanda in enumerate(comandas_do_dia):
                self.table_historico.setItem(i, 0, QTableWidgetItem(str(comanda["id"])))
                self.table_historico.setItem(i, 1, QTableWidgetItem(str(comanda["mesa_numero"])))
                self.table_historico.setItem(i, 2, QTableWidgetItem(comanda["status"]))
                self.table_historico.setItem(i, 3, QTableWidgetItem(f"R$ {comanda['total']:.2f}"))
                self.table_historico.setItem(i, 4, QTableWidgetItem(str(comanda["data_abertura"])))
                self.table_historico.setItem(i, 5, QTableWidgetItem(str(comanda.get("data_fechamento", ""))))
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar relatórios: {e}")
            
    def nova_comanda(self):
        """Abre nova comanda"""
        # Implementar diálogo para selecionar mesa
        pass
        
    def selecionar_comanda(self):
        """Seleciona uma comanda da lista"""
        current_row = self.table_comandas.currentRow()
        if current_row >= 0:
            comanda_id = int(self.table_comandas.item(current_row, 0).text())
            self.carregar_detalhes_comanda(comanda_id)
            
    def selecionar_pedido_online(self):
        """Seleciona um pedido online da lista"""
        current_row = self.table_pedidos_online.currentRow()
        if current_row >= 0:
            pedido_id = int(self.table_pedidos_online.item(current_row, 0).text())
            self.carregar_detalhes_pedido_online(pedido_id)
            
    def carregar_detalhes_comanda(self, comanda_id):
        """Carrega detalhes de uma comanda"""
        try:
            comanda = self.api_client.obter_comanda(comanda_id)
            self.comanda_atual = comanda
            
            self.lbl_mesa.setText(str(comanda["mesa"]["numero"]))
            self.lbl_status.setText(comanda["status"])
            self.lbl_total.setText(f"R$ {comanda['total']:.2f}")
            
            # Carregar itens
            itens = comanda["itens"]
            self.table_itens.setRowCount(len(itens))
            
            for i, item in enumerate(itens):
                self.table_itens.setItem(i, 0, QTableWidgetItem(item["produto"]["nome"]))
                self.table_itens.setItem(i, 1, QTableWidgetItem(str(item["quantidade"])))
                self.table_itens.setItem(i, 2, QTableWidgetItem(f"R$ {item['preco_unitario']:.2f}"))
                subtotal = item["quantidade"] * item["preco_unitario"]
                self.table_itens.setItem(i, 3, QTableWidgetItem(f"R$ {subtotal:.2f}"))
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar comanda: {e}")
            
    def carregar_detalhes_pedido_online(self, pedido_id):
        """Carrega detalhes de um pedido online"""
        try:
            pedido = self.api_client.obter_pedido_online(pedido_id)
            self.pedido_online_atual = pedido
            
            self.lbl_cliente.setText(pedido["nome_cliente"])
            self.lbl_telefone.setText(pedido["telefone"])
            self.lbl_endereco.setText(pedido["endereco"])
            self.lbl_pagamento.setText(pedido["forma_pagamento"].upper())
            self.lbl_status_pedido.setText(pedido["status"])
            self.lbl_total_pedido.setText(f"R$ {pedido['total']:.2f}")
            self.txt_observacoes_pedido.setPlainText(pedido.get("observacoes", ""))
            
            # Carregar itens
            itens = pedido["itens"]
            self.table_itens_pedido.setRowCount(len(itens))
            
            for i, item in enumerate(itens):
                self.table_itens_pedido.setItem(i, 0, QTableWidgetItem(item["produto"]["nome"]))
                self.table_itens_pedido.setItem(i, 1, QTableWidgetItem(str(item["quantidade"])))
                self.table_itens_pedido.setItem(i, 2, QTableWidgetItem(f"R$ {item['preco_unitario']:.2f}"))
                subtotal = item["quantidade"] * item["preco_unitario"]
                self.table_itens_pedido.setItem(i, 3, QTableWidgetItem(f"R$ {subtotal:.2f}"))
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar pedido online: {e}")
            
    def fechar_comanda(self):
        """Fecha a comanda atual"""
        if not self.comanda_atual:
            QMessageBox.warning(self, "Aviso", "Nenhuma comanda selecionada")
            return
            
        try:
            self.api_client.fechar_comanda(self.comanda_atual["id"])
            QMessageBox.information(self, "Sucesso", "Comanda fechada com sucesso")
            self.atualizar_comandas()
            self.comanda_atual = None
            self.limpar_detalhes_comanda()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao fechar comanda: {e}")
            
    def finalizar_comanda(self):
        """Finaliza o pagamento da comanda"""
        if not self.comanda_atual:
            QMessageBox.warning(self, "Aviso", "Nenhuma comanda selecionada")
            return
            
        try:
            self.api_client.finalizar_comanda(self.comanda_atual["id"])
            QMessageBox.information(self, "Sucesso", "Pagamento finalizado com sucesso")
            self.atualizar_comandas()
            self.comanda_atual = None
            self.limpar_detalhes_comanda()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao finalizar comanda: {e}")
            
    def limpar_detalhes_comanda(self):
        """Limpa os detalhes da comanda"""
        self.lbl_mesa.setText("-")
        self.lbl_status.setText("-")
        self.lbl_total.setText("R$ 0,00")
        self.table_itens.setRowCount(0)
        
    def limpar_detalhes_pedido_online(self):
        """Limpa os detalhes do pedido online"""
        self.lbl_cliente.setText("-")
        self.lbl_telefone.setText("-")
        self.lbl_endereco.setText("-")
        self.lbl_pagamento.setText("-")
        self.lbl_status_pedido.setText("-")
        self.lbl_total_pedido.setText("R$ 0,00")
        self.txt_observacoes_pedido.clear()
        self.table_itens_pedido.setRowCount(0)
        
    def cadastrar_produto(self):
        """Cadastra um novo produto"""
        nome = self.txt_nome_produto.text()
        preco = self.spin_preco.value()
        categoria = self.combo_categoria.currentText()
        descricao = self.txt_descricao.toPlainText()
        
        if not nome or preco <= 0:
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos obrigatórios")
            return
            
        try:
            self.api_client.criar_produto(nome, preco, categoria, descricao)
            QMessageBox.information(self, "Sucesso", "Produto cadastrado com sucesso")
            self.limpar_form_produto()
            self.atualizar_produtos()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao cadastrar produto: {e}")
            
    def limpar_form_produto(self):
        """Limpa o formulário de produto"""
        self.txt_nome_produto.clear()
        self.spin_preco.setValue(0)
        self.combo_categoria.setCurrentText("")
        self.txt_descricao.clear()
        
    def cadastrar_mesa(self):
        """Cadastra uma nova mesa"""
        numero = self.spin_numero_mesa.value()
        
        if numero <= 0:
            QMessageBox.warning(self, "Aviso", "Número da mesa deve ser maior que zero")
            return
            
        try:
            self.api_client.criar_mesa(numero)
            QMessageBox.information(self, "Sucesso", "Mesa cadastrada com sucesso")
            self.spin_numero_mesa.setValue(1)
            self.atualizar_mesas()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao cadastrar mesa: {e}")
            
    def ver_comanda(self, comanda):
        """Visualiza detalhes de uma comanda"""
        self.carregar_detalhes_comanda(comanda["id"])
        self.tab_widget.setCurrentIndex(0)  # Vai para aba de comandas
        
    def ver_pedido_online(self, pedido):
        """Visualiza detalhes de um pedido online"""
        self.carregar_detalhes_pedido_online(pedido["id"])
        self.tab_widget.setCurrentIndex(3)  # Vai para aba de pedidos online
        
    def abrir_comanda_mesa(self, mesa):
        """Abre comanda para uma mesa"""
        try:
            self.api_client.criar_comanda(mesa["id"])
            QMessageBox.information(self, "Sucesso", f"Comanda aberta para mesa {mesa['numero']}")
            self.atualizar_comandas()
            self.atualizar_mesas()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao abrir comanda: {e}")
            
    def adicionar_produto_comanda(self):
        """Adiciona produto à comanda atual"""
        if not self.comanda_atual:
            QMessageBox.warning(self, "Aviso", "Nenhuma comanda selecionada")
            return
            
        try:
            # Buscar produtos disponíveis
            produtos = self.api_client.listar_produtos()
            
            if not produtos:
                QMessageBox.warning(self, "Aviso", "Nenhum produto cadastrado")
                return
                
            # Abrir diálogo para selecionar produto
            dialog = AdicionarProdutoDialog(produtos, self)
            if dialog.exec_() == QDialog.Accepted:
                produto, quantidade = dialog.get_produto_quantidade()
                
                if produto and quantidade > 0:
                    # Adicionar item à comanda
                    self.api_client.adicionar_item_comanda(
                        self.comanda_atual["id"],
                        produto["id"],
                        quantidade
                    )
                    
                    QMessageBox.information(self, "Sucesso", 
                                          f"Produto '{produto['nome']}' adicionado à comanda")
                    
                    # Atualizar detalhes da comanda
                    self.carregar_detalhes_comanda(self.comanda_atual["id"])
                    self.atualizar_comandas()
                    
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao adicionar produto: {e}")
            
    # Funções para gerenciar pedidos online
    def confirmar_pedido(self):
        """Confirma um pedido online"""
        if not self.pedido_online_atual:
            QMessageBox.warning(self, "Aviso", "Nenhum pedido selecionado")
            return
            
        try:
            self.api_client.atualizar_status_pedido_online(self.pedido_online_atual["id"], "confirmado")
            QMessageBox.information(self, "Sucesso", "Pedido confirmado com sucesso")
            self.atualizar_pedidos_online()
            self.carregar_detalhes_pedido_online(self.pedido_online_atual["id"])
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao confirmar pedido: {e}")
            
    def preparando_pedido(self):
        """Marca pedido como em preparação"""
        if not self.pedido_online_atual:
            QMessageBox.warning(self, "Aviso", "Nenhum pedido selecionado")
            return
            
        try:
            self.api_client.atualizar_status_pedido_online(self.pedido_online_atual["id"], "preparando")
            QMessageBox.information(self, "Sucesso", "Pedido marcado como em preparação")
            self.atualizar_pedidos_online()
            self.carregar_detalhes_pedido_online(self.pedido_online_atual["id"])
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao atualizar status: {e}")
            
    def entregando_pedido(self):
        """Marca pedido como entregando"""
        if not self.pedido_online_atual:
            QMessageBox.warning(self, "Aviso", "Nenhum pedido selecionado")
            return
            
        try:
            self.api_client.atualizar_status_pedido_online(self.pedido_online_atual["id"], "entregando")
            QMessageBox.information(self, "Sucesso", "Pedido marcado como entregando")
            self.atualizar_pedidos_online()
            self.carregar_detalhes_pedido_online(self.pedido_online_atual["id"])
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao atualizar status: {e}")
            
    def entregue_pedido(self):
        """Marca pedido como entregue"""
        if not self.pedido_online_atual:
            QMessageBox.warning(self, "Aviso", "Nenhum pedido selecionado")
            return
            
        try:
            self.api_client.atualizar_status_pedido_online(self.pedido_online_atual["id"], "entregue")
            QMessageBox.information(self, "Sucesso", "Pedido marcado como entregue")
            self.atualizar_pedidos_online()
            self.pedido_online_atual = None
            self.limpar_detalhes_pedido_online()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao atualizar status: {e}") 

    def cancelar_comanda(self):
        if not hasattr(self, 'comanda_atual') or not self.comanda_atual:
            QMessageBox.warning(self, "Atenção", "Selecione uma comanda para cancelar.")
            return
        confirm = QMessageBox.question(self, "Cancelar Comanda", "Tem certeza que deseja cancelar esta comanda?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                self.api_client.cancelar_comanda(self.comanda_atual["id"])
                QMessageBox.information(self, "Sucesso", "Comanda cancelada com sucesso.")
                self.atualizar_comandas()
                self.limpar_detalhes_comanda()
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao cancelar comanda: {e}")

    def cancelar_pedido_online(self):
        if not hasattr(self, 'pedido_online_atual') or not self.pedido_online_atual:
            QMessageBox.warning(self, "Atenção", "Selecione um pedido para cancelar.")
            return
        confirm = QMessageBox.question(self, "Cancelar Pedido", "Tem certeza que deseja cancelar este pedido?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                self.api_client.atualizar_status_pedido_online(self.pedido_online_atual["id"], "cancelado")
                QMessageBox.information(self, "Sucesso", "Pedido cancelado com sucesso.")
                self.atualizar_pedidos_online()
                self.limpar_detalhes_pedido_online()
            except Exception as e:
                QMessageBox.warning(self, "Erro", f"Erro ao cancelar pedido: {e}") 
    
    def verificar_novo_dia(self):
        """Verifica se é um novo dia e limpa as telas se necessário"""
        data_atual = date.today()
        
        if self.ultima_data is None:
            # Primeira execução
            self.ultima_data = data_atual
        elif self.ultima_data != data_atual:
            # Novo dia detectado
            self.limpar_todas_telas()
            self.ultima_data = data_atual
            QMessageBox.information(self, "Novo Dia", "Detectado novo dia. Todas as telas foram limpas.")
    
    def limpar_todas_telas(self):
        """Limpa todas as telas, tabelas e formulários"""
        # Limpar detalhes de comanda
        self.comanda_atual = None
        self.limpar_detalhes_comanda()
        if hasattr(self, 'table_comandas'):
            self.table_comandas.setRowCount(0)
        
        # Limpar detalhes de pedido online
        self.pedido_online_atual = None
        self.limpar_detalhes_pedido_online()
        if hasattr(self, 'table_pedidos_online'):
            self.table_pedidos_online.setRowCount(0)
        
        # Limpar formulário de produto
        self.limpar_form_produto()
        if hasattr(self, 'table_produtos'):
            self.table_produtos.setRowCount(0)
        
        # Limpar formulário de mesa
        if hasattr(self, 'spin_numero_mesa'):
            self.spin_numero_mesa.setValue(1)
        if hasattr(self, 'table_mesas'):
            self.table_mesas.setRowCount(0)
        
        # Limpar histórico de comandas
        if hasattr(self, 'table_historico'):
            self.table_historico.setRowCount(0)
        
        # Limpar observações de pedido online
        if hasattr(self, 'txt_observacoes_pedido'):
            self.txt_observacoes_pedido.clear()
        
        # Limpar labels de estatísticas
        if hasattr(self, 'lbl_total_comandas'):
            self.lbl_total_comandas.setText("0")
        if hasattr(self, 'lbl_comandas_abertas'):
            self.lbl_comandas_abertas.setText("0")
        if hasattr(self, 'lbl_comandas_fechadas'):
            self.lbl_comandas_fechadas.setText("0")
        if hasattr(self, 'lbl_faturamento_dia'):
            self.lbl_faturamento_dia.setText("R$ 0,00")
        
        # Limpar gráficos
        if hasattr(self, 'charts_widget'):
            self.charts_widget.limpar_graficos() if hasattr(self.charts_widget, 'limpar_graficos') else None
        
        QMessageBox.information(self, "Limpeza", "Todas as telas foram limpas com sucesso.")
    
    def baixar_relatorio(self):
        """Baixa relatório em formato CSV"""
        try:
            # Obter dados para o relatório
            comandas = self.api_client.listar_comandas()
            pedidos_online = self.api_client.listar_pedidos_online()
            produtos = self.api_client.listar_produtos()
            
            # Solicitar local para salvar
            filename, _ = QFileDialog.getSaveFileName(
                self, 
                "Salvar Relatório", 
                f"relatorio_padaria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "Arquivos CSV (*.csv)"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Cabeçalho
                    writer.writerow(['RELATÓRIO PADARIA - ' + datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
                    writer.writerow([])
                    
                    # Estatísticas gerais
                    writer.writerow(['ESTATÍSTICAS GERAIS'])
                    writer.writerow(['Total de Comandas', len(comandas)])
                    writer.writerow(['Comandas Abertas', len([c for c in comandas if c['status'] == 'aberta'])])
                    writer.writerow(['Comandas Fechadas', len([c for c in comandas if c['status'] == 'fechada'])])
                    writer.writerow(['Comandas Canceladas', len([c for c in comandas if c['status'] == 'cancelada'])])
                    writer.writerow(['Total de Pedidos Online', len(pedidos_online)])
                    writer.writerow(['Faturamento Total', f"R$ {sum([c['total'] for c in comandas if c['status'] == 'fechada']):.2f}"])
                    writer.writerow([])
                    
                    # Comandas
                    writer.writerow(['COMANDA', 'MESA', 'STATUS', 'TOTAL', 'ITENS', 'DATA ABERTURA', 'DATA FECHAMENTO'])
                    for comanda in comandas:
                        writer.writerow([
                            comanda['id'],
                            comanda['mesa_numero'],
                            comanda['status'],
                            f"R$ {comanda['total']:.2f}",
                            comanda['quantidade_itens'],
                            comanda['data_abertura'],
                            comanda.get('data_fechamento', '')
                        ])
                    writer.writerow([])
                    
                    # Pedidos Online
                    writer.writerow(['PEDIDO ONLINE', 'CLIENTE', 'TELEFONE', 'STATUS', 'TOTAL', 'ITENS', 'DATA PEDIDO'])
                    for pedido in pedidos_online:
                        writer.writerow([
                            pedido['id'],
                            pedido['nome_cliente'],
                            pedido['telefone'],
                            pedido['status'],
                            f"R$ {pedido['total']:.2f}",
                            pedido['quantidade_itens'],
                            pedido['data_pedido']
                        ])
                    writer.writerow([])
                    
                    # Produtos
                    writer.writerow(['PRODUTO', 'CATEGORIA', 'PREÇO', 'DESCRIÇÃO'])
                    for produto in produtos:
                        writer.writerow([
                            produto['nome'],
                            produto['categoria'],
                            f"R$ {produto['preco']:.2f}",
                            produto.get('descricao', '')
                        ])
                
                QMessageBox.information(self, "Sucesso", f"Relatório salvo com sucesso em:\n{filename}")
                
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao gerar relatório: {e}") 