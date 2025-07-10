from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QComboBox, QPushButton, QDateEdit
from PyQt5.QtCore import Qt, QDate
try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib não está disponível. Instale com: pip install matplotlib numpy")
from collections import Counter, defaultdict
from datetime import datetime, timedelta

class ChartsWidget(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Gráficos de Relatórios")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Controles de período
        period_group = QGroupBox("Período de Análise")
        period_layout = QHBoxLayout(period_group)
        
        # Seletor de período
        period_layout.addWidget(QLabel("Período:"))
        self.combo_periodo = QComboBox()
        self.combo_periodo.addItems(["Hoje", "Última Semana", "Último Mês", "Personalizado"])
        self.combo_periodo.currentTextChanged.connect(self.on_periodo_changed)
        period_layout.addWidget(self.combo_periodo)
        
        # Seletor de data (inicialmente desabilitado)
        period_layout.addWidget(QLabel("Data:"))
        self.date_selector = QDateEdit()
        self.date_selector.setDate(QDate.currentDate())
        self.date_selector.setCalendarPopup(True)
        self.date_selector.setEnabled(False)
        period_layout.addWidget(self.date_selector)
        
        # Botão atualizar
        self.btn_atualizar = QPushButton("Atualizar Gráficos")
        self.btn_atualizar.clicked.connect(self.atualizar_graficos)
        period_layout.addWidget(self.btn_atualizar)
        
        period_layout.addStretch()
        layout.addWidget(period_group)
        
        if not MATPLOTLIB_AVAILABLE:
            # Se matplotlib não estiver disponível, mostrar mensagem
            error_label = QLabel("Matplotlib não está instalado.\nInstale com: pip install matplotlib numpy")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet("color: red; font-size: 14px; margin: 20px;")
            layout.addWidget(error_label)
            return
        
        # Layout para os 3 gráficos
        charts_layout = QHBoxLayout()
        
        # Gráfico 1: Pedidos Online vs Presentes
        self.chart1_group = QGroupBox("Pedidos Online vs Presentes")
        self.chart1_layout = QVBoxLayout(self.chart1_group)
        self.figure1 = Figure(figsize=(6, 4))
        self.canvas1 = FigureCanvas(self.figure1)
        self.chart1_layout.addWidget(self.canvas1)
        charts_layout.addWidget(self.chart1_group)
        
        # Gráfico 2: Produtos Mais Pedidos
        self.chart2_group = QGroupBox("Produtos Mais Pedidos")
        self.chart2_layout = QVBoxLayout(self.chart2_group)
        self.figure2 = Figure(figsize=(6, 4))
        self.canvas2 = FigureCanvas(self.figure2)
        self.chart2_layout.addWidget(self.canvas2)
        charts_layout.addWidget(self.chart2_group)
        
        # Gráfico 3: Status dos Pedidos
        self.chart3_group = QGroupBox("Status dos Pedidos")
        self.chart3_layout = QVBoxLayout(self.chart3_group)
        self.figure3 = Figure(figsize=(6, 4))
        self.canvas3 = FigureCanvas(self.figure3)
        self.chart3_layout.addWidget(self.canvas3)
        charts_layout.addWidget(self.chart3_group)
        
        layout.addLayout(charts_layout)
        
        # Status
        self.status_label = QLabel("Gráficos atualizados automaticamente")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: gray; margin: 5px;")
        layout.addWidget(self.status_label)
        
    def on_periodo_changed(self, periodo):
        """Chamado quando o período é alterado"""
        if periodo == "Personalizado":
            self.date_selector.setEnabled(True)
        else:
            self.date_selector.setEnabled(False)
        self.atualizar_graficos()
        
    def get_date_range(self):
        """Retorna o intervalo de datas baseado no período selecionado"""
        periodo = self.combo_periodo.currentText()
        hoje = datetime.now().date()
        
        if periodo == "Hoje":
            return hoje, hoje
        elif periodo == "Última Semana":
            inicio = hoje - timedelta(days=7)
            return inicio, hoje
        elif periodo == "Último Mês":
            inicio = hoje - timedelta(days=30)
            return inicio, hoje
        elif periodo == "Personalizado":
            data_selecionada = self.date_selector.date().toPyDate()
            return data_selecionada, data_selecionada
        else:
            return hoje, hoje
    
    def filter_data_by_date(self, data_list, date_field="data_abertura"):
        """Filtra dados por intervalo de datas"""
        inicio, fim = self.get_date_range()
        filtered_data = []
        
        for item in data_list:
            try:
                # Tentar diferentes formatos de data
                if isinstance(item.get(date_field), str):
                    # Se for string, tentar converter
                    if 'T' in item[date_field]:  # Formato ISO
                        item_date = datetime.fromisoformat(item[date_field].replace('Z', '+00:00')).date()
                    else:  # Formato simples
                        item_date = datetime.strptime(item[date_field], '%Y-%m-%d').date()
                else:
                    # Se já for datetime
                    item_date = item[date_field].date()
                
                if inicio <= item_date <= fim:
                    filtered_data.append(item)
            except (ValueError, TypeError, AttributeError):
                # Se não conseguir converter a data, incluir o item
                filtered_data.append(item)
        
        return filtered_data
        
    def atualizar_graficos(self):
        """Atualiza todos os gráficos com dados atuais"""
        if not MATPLOTLIB_AVAILABLE:
            return
            
        try:
            self.status_label.setText("Atualizando gráficos...")
            
            # Buscar dados
            comandas = self.api_client.listar_comandas()
            pedidos_online = self.api_client.listar_pedidos_online()
            
            # Filtrar por período
            comandas_filtradas = self.filter_data_by_date(comandas, "data_abertura")
            pedidos_filtrados = self.filter_data_by_date(pedidos_online, "data_pedido")
            
            # Atualizar cada gráfico
            self.atualizar_grafico_pedidos(comandas_filtradas, pedidos_filtrados)
            self.atualizar_grafico_produtos(comandas_filtradas, pedidos_filtrados)
            self.atualizar_grafico_status(comandas_filtradas, pedidos_filtrados)
            
            # Atualizar status
            periodo = self.combo_periodo.currentText()
            self.status_label.setText(f"Gráficos atualizados - Período: {periodo}")
            
        except Exception as e:
            print(f"Erro ao atualizar gráficos: {e}")
            self.status_label.setText(f"Erro ao atualizar gráficos: {e}")
    
    def atualizar_grafico_pedidos(self, comandas, pedidos_online):
        """Gráfico 1: Pedidos Online vs Presentes"""
        self.figure1.clear()
        ax = self.figure1.add_subplot(111)
        
        # Contar pedidos
        total_presentes = len(comandas)
        total_online = len(pedidos_online)
        
        # Dados para o gráfico
        labels = ['Pedidos Presentes', 'Pedidos Online']
        sizes = [total_presentes, total_online]
        colors = ['#ff9999', '#66b3ff']
        
        # Criar gráfico de pizza (evitar erro se tudo zero)
        if sum(sizes) == 0:
            ax.text(0.5, 0.5, 'Sem dados para o período', ha='center', va='center', fontsize=12)
            ax.set_title('Distribuição de Pedidos', fontweight='bold')
            ax.axis('off')
        else:
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            ax.set_title('Distribuição de Pedidos', fontweight='bold')
            ax.axis('equal')
            # Removido texto de legenda
        self.canvas1.draw()
    
    def atualizar_grafico_produtos(self, comandas, pedidos_online):
        """Gráfico 2: Produtos Mais Pedidos"""
        self.figure2.clear()
        ax = self.figure2.add_subplot(111)
        
        # Coletar dados de produtos
        produtos_count = Counter()
        
        # Produtos de comandas presenciais
        for comanda in comandas:
            for item in comanda.get('itens', []):
                produto_nome = item.get('produto', {}).get('nome', 'Produto Desconhecido')
                quantidade = item.get('quantidade', 1)
                produtos_count[produto_nome] += quantidade
        
        # Produtos de pedidos online
        for pedido in pedidos_online:
            for item in pedido.get('itens', []):
                produto_nome = item.get('produto', {}).get('nome', 'Produto Desconhecido')
                quantidade = item.get('quantidade', 1)
                produtos_count[produto_nome] += quantidade
        
        # Pegar os 8 produtos mais vendidos
        top_produtos = produtos_count.most_common(8)
        
        if not top_produtos:
            # Se não há dados, mostrar mensagem
            ax.text(0.5, 0.5, 'Nenhum produto vendido no período', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
            ax.set_title('Produtos Mais Pedidos', fontweight='bold')
        else:
            # Preparar dados para o gráfico
            nomes = [prod[0] for prod in top_produtos]
            quantidades = [prod[1] for prod in top_produtos]
            
            # Criar gráfico de barras
            bars = ax.barh(nomes, quantidades, color='#ff7f0e')
            
            # Adicionar valores nas barras
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                       f'{width}', ha='left', va='center', fontweight='bold')
            
            ax.set_xlabel('Quantidade Vendida')
            ax.set_title('Produtos Mais Pedidos', fontweight='bold')
            ax.invert_yaxis()  # Inverter para mostrar o mais vendido no topo
        
        self.figure2.tight_layout()
        self.canvas2.draw()
    
    def atualizar_grafico_status(self, comandas, pedidos_online):
        """Gráfico 3: Status dos Pedidos (Cancelados, Abertos, Fechados)"""
        self.figure3.clear()
        ax = self.figure3.add_subplot(111)
        
        # Contar status das comandas
        status_comandas = Counter()
        for comanda in comandas:
            status = comanda.get('status', 'desconhecido')
            status_comandas[status] += 1
        
        # Contar status dos pedidos online
        status_online = Counter()
        for pedido in pedidos_online:
            status = pedido.get('status', 'desconhecido')
            status_online[status] += 1
        
        # Combinar dados
        total_abertos = status_comandas.get('aberta', 0)
        total_fechados = status_comandas.get('fechada', 0) + status_comandas.get('aguardando_pagamento', 0)
        total_cancelados = status_comandas.get('cancelado', 0) + status_online.get('cancelado', 0)
        
        # Dados para o gráfico
        labels = ['Abertos', 'Fechados', 'Cancelados']
        sizes = [total_abertos, total_fechados, total_cancelados]
        colors = ['#ffcc5c', '#96ceb4', '#ff6f69']
        
        # Criar gráfico de pizza (evitar erro se tudo zero)
        if sum(sizes) == 0:
            ax.text(0.5, 0.5, 'Sem dados para o período', ha='center', va='center', fontsize=12)
            ax.set_title('Status dos Pedidos', fontweight='bold')
            ax.axis('off')
        else:
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            ax.set_title('Status dos Pedidos', fontweight='bold')
            ax.axis('equal')
            # Removido texto de legenda
        self.canvas3.draw() 