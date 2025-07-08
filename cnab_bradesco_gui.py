import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QFileDialog, QTextEdit, QLabel, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox,
                            QFrame, QSplitter, QStatusBar, QProgressBar, QMessageBox,
                            QTabWidget, QScrollArea, QSizePolicy, QSlider, QToolButton,
                            QGridLayout, QDialog, QLineEdit, QComboBox, QSpinBox,
                            QFormLayout, QDialogButtonBox, QCheckBox)
from PyQt5.QtCore import Qt, QSize, QSettings
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QPixmap
import locale

from cnab_bradesco import CNABBradesco

# Constantes de estilo - Tema Único
TEMA_ATUAL = {
    'COR_PRIMARIA': '#0063B1',
    'COR_SECUNDARIA': '#FFFFFF',
    'COR_DESTAQUE': '#D93025',
    'COR_FUNDO': '#F5F7FA',
    'COR_TEXTO': '#212529',
    'COR_BOTAO_HOVER': '#004D8C',
    'COR_CABECALHO': '#0063B1',
    'COR_TABELA_HEADER': '#E9ECEF',
    'COR_TABELA_LINHA_ALTERNADA': '#F8F9FA'
}


class EstiloBotao(QPushButton):
    def __init__(self, texto, primario=True):
        super().__init__(texto)
        self.primario = primario
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(40)
        self.setFont(QFont('Segoe UI', 10))
        self.aplicar_estilo()
        
    def aplicar_estilo(self):
        if self.primario:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: bold;
                    text-align: center;
                    min-height: 40px;
                }}
                QPushButton:hover {{
                    background-color: {TEMA_ATUAL['COR_BOTAO_HOVER']};
                }}
                QPushButton:pressed {{
                    background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                    padding: 9px 15px 7px 17px;
                }}
                QPushButton:disabled {{
                    background-color: #A0AEC0;
                    color: #EDF2F7;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                    color: {TEMA_ATUAL['COR_TEXTO']};
                    border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                    border-radius: 8px;
                    padding: 8px 16px;
                    text-align: center;
                    min-height: 40px;
                }}
                QPushButton:hover {{
                    background-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                }}
                QPushButton:pressed {{
                    background-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                    padding: 9px 15px 7px 17px;
                }}
                QPushButton:disabled {{
                    background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                    color: #A0AEC0;
                    border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                    opacity: 0.6;
                }}
            """)
            
    def update_tema(self):
        self.aplicar_estilo()


class EditorGraficoDialog(QDialog):
    """Dialog para edição gráfica dos campos NOSSO_NUMERO, CODIGO_EMPRESA e SEU_NUMERO (parte antes da barra)"""
    
    def __init__(self, processador, parent=None):
        super().__init__(parent)
        self.processador = processador
        self.alteracoes_realizadas = False
        self.dados_editados = []
        
        # Copiar dados originais
        self.dados_editados = [detalhe.copy() for detalhe in self.processador.detalhes]
        
        self.setup_ui()
        self.carregar_dados()
        
    def setup_ui(self):
        self.setWindowTitle("Editor Gráfico - NOSSO_NUMERO, CODIGO_EMPRESA e SEU_NUMERO")
        self.setMinimumSize(1400, 600)  # Mais largo e menos alto
        self.setModal(True)
        
        # Layout principal vertical
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)
        
        # Cabeçalho (topo, largura total)
        self.criar_cabecalho(main_layout)
        
        # Área principal horizontal com splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        
        # Painel esquerdo - Tabela (70% do espaço)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 8, 0)
        left_layout.setSpacing(12)
        
        # Área de filtros no painel esquerdo
        self.criar_area_filtros(left_layout)
        
        # Tabela de edição no painel esquerdo
        self.criar_tabela_edicao(left_layout)
        
        # Painel direito - Controles (30% do espaço)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(8, 0, 0, 0)
        right_layout.setSpacing(12)
        
        # Scroll area para os controles do painel direito
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {TEMA_ATUAL['COR_FUNDO']};
            }}
            QScrollBar:vertical {{
                border: none;
                background: {TEMA_ATUAL['COR_TABELA_HEADER']};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Widget para conteúdo do scroll
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(12)
        
        # Adicionar controles ao scroll
        self.criar_area_edicao_lote(scroll_layout)
        self.criar_area_importacao_planilha(scroll_layout)
        
        # Espaçador para empurrar conteúdo para o topo
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        right_layout.addWidget(scroll_area)
        
        # Adicionar painéis ao splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        # Definir proporções: 70% esquerda, 30% direita
        splitter.setSizes([700, 300])
        splitter.setStretchFactor(0, 7)  # Painel esquerdo mais flexível
        splitter.setStretchFactor(1, 3)  # Painel direito menos flexível
        
        main_layout.addWidget(splitter, 1)
        
        # Botões de ação (rodapé, largura total)
        self.criar_botoes_acao(main_layout)
        
        # Aplicar estilo
        self.aplicar_estilo()
        
    def criar_cabecalho(self, layout):
        # Frame do cabeçalho
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                border-radius: 8px;
                padding: 16px;
            }}
        """)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 12, 20, 12)
        
        # Ícone
        icon_label = QLabel("✏️")
        icon_label.setStyleSheet("font-size: 24px; color: white;")
        header_layout.addWidget(icon_label)
        
        # Título e informações
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(16, 0, 0, 0)
        title_layout.setSpacing(4)
        
        title_label = QLabel("Editor Gráfico de Campos")
        title_label.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
            font-family: 'Segoe UI';
        """)
        
        subtitle_label = QLabel("Edição dos campos NOSSO_NUMERO, CODIGO_EMPRESA e SEU_NUMERO (parte antes da barra)")
        subtitle_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            font-size: 14px;
            font-family: 'Segoe UI';
        """)
        
        # Contador de registros
        self.contador_label = QLabel(f"Total de registros: {len(self.dados_editados)}")
        self.contador_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            font-size: 12px;
            font-family: 'Segoe UI';
        """)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        title_layout.addWidget(self.contador_label)
        
        header_layout.addWidget(title_widget, 1)
        layout.addWidget(header_frame)
        
    def criar_area_filtros(self, layout):
        # Frame de filtros
        filter_frame = QFrame()
        filter_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(16, 12, 16, 12)
        filter_layout.setSpacing(12)
        
        # Filtro por Nosso Número
        filter_layout.addWidget(QLabel("🔍 Buscar:"))
        
        self.filtro_nosso_numero = QLineEdit()
        self.filtro_nosso_numero.setPlaceholderText("Nosso Número...")
        self.filtro_nosso_numero.textChanged.connect(self.filtrar_dados)
        self.filtro_nosso_numero.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px;
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                border-radius: 4px;
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 2px solid {TEMA_ATUAL['COR_PRIMARIA']};
            }}
        """)
        filter_layout.addWidget(self.filtro_nosso_numero)
        
        # Filtro por Código da Empresa
        self.filtro_codigo_empresa = QLineEdit()
        self.filtro_codigo_empresa.setPlaceholderText("Código da Empresa...")
        self.filtro_codigo_empresa.textChanged.connect(self.filtrar_dados)
        self.filtro_codigo_empresa.setStyleSheet(self.filtro_nosso_numero.styleSheet())
        filter_layout.addWidget(self.filtro_codigo_empresa)
        
        # Filtro por Seu Número
        self.filtro_seu_numero = QLineEdit()
        self.filtro_seu_numero.setPlaceholderText("Seu Número...")
        self.filtro_seu_numero.textChanged.connect(self.filtrar_dados)
        self.filtro_seu_numero.setStyleSheet(self.filtro_nosso_numero.styleSheet())
        filter_layout.addWidget(self.filtro_seu_numero)
        
        # Botão limpar filtros
        btn_limpar = QPushButton("🗑️ Limpar")
        btn_limpar.clicked.connect(self.limpar_filtros)
        btn_limpar.setStyleSheet(f"""
            QPushButton {{
                background-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                color: {TEMA_ATUAL['COR_TEXTO']};
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                color: white;
            }}
        """)
        filter_layout.addWidget(btn_limpar)
        
        filter_layout.addStretch()
        layout.addWidget(filter_frame)
        
    def criar_tabela_edicao(self, layout):
        # Frame da tabela
        table_frame = QFrame()
        table_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(12, 12, 12, 12)
        
        # Label da tabela
        table_label = QLabel("📋 Registros para Edição")
        table_label.setStyleSheet(f"""
            color: {TEMA_ATUAL['COR_TEXTO']};
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 8px;
        """)
        table_layout.addWidget(table_label)
        
        # Tabela
        self.tabela_edicao = QTableWidget()
        self.tabela_edicao.setColumnCount(6)
        self.tabela_edicao.setHorizontalHeaderLabels([
            "Seq", "Nosso Número", "Código Empresa", "Seu Número", "Valor", "Vencimento"
        ])
        
        # Configurar tabela
        self.tabela_edicao.setAlternatingRowColors(True)
        self.tabela_edicao.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_edicao.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela_edicao.horizontalHeader().setStretchLastSection(True)
        self.tabela_edicao.verticalHeader().setVisible(False)
        
        # Configurar colunas editáveis
        self.tabela_edicao.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        
        # Conectar evento de edição
        self.tabela_edicao.itemChanged.connect(self.item_editado)
        
        # Estilo da tabela
        self.tabela_edicao.setStyleSheet(f"""
            QTableWidget {{
                background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                color: {TEMA_ATUAL['COR_TEXTO']};
                gridline-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                border-radius: 4px;
                selection-background-color: {TEMA_ATUAL['COR_PRIMARIA']};
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
            }}
            QTableWidget::item:selected {{
                background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                color: white;
            }}
            QHeaderView::section {{
                background-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                color: {TEMA_ATUAL['COR_TEXTO']};
                padding: 10px;
                border: none;
                font-weight: bold;
                text-align: center;
            }}
        """)
        
        table_layout.addWidget(self.tabela_edicao, 1)
        layout.addWidget(table_frame, 1)
        
    def criar_area_edicao_lote(self, layout):
        # Frame de edição em lote
        lote_frame = QFrame()
        lote_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        
        lote_layout = QVBoxLayout(lote_frame)
        lote_layout.setContentsMargins(12, 8, 12, 8)
        lote_layout.setSpacing(8)
        
        # Título
        lote_label = QLabel("🔧 Edição em Lote")
        lote_label.setStyleSheet(f"""
            color: {TEMA_ATUAL['COR_TEXTO']};
            font-size: 13px;
            font-weight: bold;
        """)
        lote_layout.addWidget(lote_label)
        
        # Seção Nosso Número
        nosso_section = QVBoxLayout()
        nosso_section.setSpacing(4)
        
        # Label Nosso Número
        nosso_label = QLabel("Nosso Número:")
        nosso_label.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-size: 12px; font-weight: bold;")
        nosso_section.addWidget(nosso_label)
        
        self.novo_nosso_numero = QLineEdit()
        self.novo_nosso_numero.setPlaceholderText("Novo valor para todos...")
        self.novo_nosso_numero.setStyleSheet(f"""
            QLineEdit {{
                padding: 6px;
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                border-radius: 4px;
                font-size: 12px;
            }}
        """)
        nosso_section.addWidget(self.novo_nosso_numero)
        
        btn_aplicar_nosso = QPushButton("Aplicar a Todos")
        btn_aplicar_nosso.clicked.connect(self.aplicar_nosso_numero_lote)
        btn_aplicar_nosso.setStyleSheet(f"""
            QPushButton {{
                background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                color: white;
                border: none;
                padding: 6px 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {TEMA_ATUAL['COR_BOTAO_HOVER']};
            }}
        """)
        nosso_section.addWidget(btn_aplicar_nosso)
        
        lote_layout.addLayout(nosso_section)
        
        # Separador horizontal
        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setStyleSheet(f"color: {TEMA_ATUAL['COR_TABELA_HEADER']};")
        lote_layout.addWidget(separador)
        
        # Seção Código da Empresa
        codigo_section = QVBoxLayout()
        codigo_section.setSpacing(4)
        
        # Label Código Empresa
        codigo_label = QLabel("Código Empresa:")
        codigo_label.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-size: 12px; font-weight: bold;")
        codigo_section.addWidget(codigo_label)
        
        self.novo_codigo_empresa = QLineEdit()
        self.novo_codigo_empresa.setPlaceholderText("Novo valor para todos...")
        self.novo_codigo_empresa.setStyleSheet(self.novo_nosso_numero.styleSheet())
        codigo_section.addWidget(self.novo_codigo_empresa)
        
        btn_aplicar_codigo = QPushButton("Aplicar a Todos")
        btn_aplicar_codigo.clicked.connect(self.aplicar_codigo_empresa_lote)
        btn_aplicar_codigo.setStyleSheet(btn_aplicar_nosso.styleSheet())
        codigo_section.addWidget(btn_aplicar_codigo)
        
        lote_layout.addLayout(codigo_section)
        
        # Separador horizontal
        separador2 = QFrame()
        separador2.setFrameShape(QFrame.HLine)
        separador2.setStyleSheet(f"color: {TEMA_ATUAL['COR_TABELA_HEADER']};")
        lote_layout.addWidget(separador2)
        
        # Seção Seu Número
        seu_section = QVBoxLayout()
        seu_section.setSpacing(4)
        
        # Label Seu Número
        seu_label = QLabel("Seu Número (remove barra e dígitos):")
        seu_label.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-size: 12px; font-weight: bold;")
        seu_section.addWidget(seu_label)
        
        self.novo_seu_numero = QLineEdit()
        self.novo_seu_numero.setPlaceholderText("Novo valor (remove barra/dígitos)...")
        self.novo_seu_numero.setStyleSheet(self.novo_nosso_numero.styleSheet())
        seu_section.addWidget(self.novo_seu_numero)
        
        btn_aplicar_seu = QPushButton("Aplicar a Todos")
        btn_aplicar_seu.clicked.connect(self.aplicar_seu_numero_lote)
        btn_aplicar_seu.setStyleSheet(btn_aplicar_nosso.styleSheet())
        seu_section.addWidget(btn_aplicar_seu)
        
        lote_layout.addLayout(seu_section)
        layout.addWidget(lote_frame)
        
    def criar_area_importacao_planilha(self, layout):
        """Cria área para importação de planilha com mapeamentos"""
        # Frame de importação
        import_frame = QFrame()
        import_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        
        import_layout = QVBoxLayout(import_frame)
        import_layout.setContentsMargins(12, 8, 12, 8)
        import_layout.setSpacing(8)
        
        # Título
        import_label = QLabel("📊 Importar Mapeamentos")
        import_label.setStyleSheet(f"""
            color: {TEMA_ATUAL['COR_TEXTO']};
            font-size: 13px;
            font-weight: bold;
        """)
        import_layout.addWidget(import_label)
        
        # Descrição compacta
        desc_label = QLabel("Planilha Excel com colunas para mapeamentos de NOSSO_NUMERO ou SEU_NUMERO")
        desc_label.setStyleSheet(f"""
            color: {TEMA_ATUAL['COR_TEXTO']};
            font-size: 11px;
            font-style: italic;
            margin-bottom: 4px;
        """)
        desc_label.setWordWrap(True)
        import_layout.addWidget(desc_label)
        
        # Seletor de tipo de mapeamento
        tipo_layout = QHBoxLayout()
        tipo_layout.setSpacing(8)
        
        tipo_label = QLabel("Tipo:")
        tipo_label.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-size: 11px; font-weight: bold;")
        tipo_layout.addWidget(tipo_label)
        
        self.tipo_mapeamento = QComboBox()
        self.tipo_mapeamento.addItems([
            "NOSSO_NUMERO (colunas: NOSSO_NUMERO_ATUAL, NOSSO_NUMERO_CORRIGIDO)",
            "SEU_NUMERO (colunas: SEU_NUMERO_COMPLETO_ATUAL, SEU_NUMERO_NOVO)"
        ])
        self.tipo_mapeamento.setStyleSheet(f"""
            QComboBox {{
                padding: 4px;
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                border-radius: 4px;
                font-size: 10px;
            }}
        """)
        self.tipo_mapeamento.currentTextChanged.connect(self.atualizar_preview_tipo_mapeamento)
        tipo_layout.addWidget(self.tipo_mapeamento)
        
        import_layout.addLayout(tipo_layout)
        
        # Campo para mostrar arquivo selecionado
        self.planilha_selecionada = QLabel("Nenhuma planilha selecionada")
        self.planilha_selecionada.setStyleSheet(f"""
            QLabel {{
                color: {TEMA_ATUAL['COR_TEXTO']};
                background-color: {TEMA_ATUAL['COR_FUNDO']};
                padding: 6px;
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                border-radius: 4px;
                font-size: 11px;
            }}
        """)
        import_layout.addWidget(self.planilha_selecionada)
        
        # Botões em layout vertical para economizar espaço
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(4)
        
        # Botão para selecionar planilha
        btn_selecionar_planilha = QPushButton("📁 Selecionar")
        btn_selecionar_planilha.clicked.connect(self.selecionar_planilha_mapeamento)
        btn_selecionar_planilha.setStyleSheet(f"""
            QPushButton {{
                background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                color: white;
                border: none;
                padding: 6px 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {TEMA_ATUAL['COR_BOTAO_HOVER']};
            }}
        """)
        btn_layout.addWidget(btn_selecionar_planilha)
        
        # Botão para aplicar mapeamentos
        self.btn_aplicar_mapeamentos = QPushButton("🔄 Aplicar")
        self.btn_aplicar_mapeamentos.clicked.connect(self.aplicar_mapeamentos_planilha)
        self.btn_aplicar_mapeamentos.setEnabled(False)
        self.btn_aplicar_mapeamentos.setStyleSheet(f"""
            QPushButton {{
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 6px 8px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 140px;
            }}
            QPushButton:hover {{
                background-color: #2ecc71;
            }}
            QPushButton:disabled {{
                background-color: #A0AEC0;
                color: #EDF2F7;
            }}
        """)
        btn_layout.addWidget(self.btn_aplicar_mapeamentos)
        
        import_layout.addLayout(btn_layout)
        
        # Área de preview dos mapeamentos (mais compacta)
        self.preview_mapeamentos = QLabel("Preview aparecerá após selecionar planilha")
        self.preview_mapeamentos.setStyleSheet(f"""
            QLabel {{
                color: {TEMA_ATUAL['COR_TEXTO']};
                background-color: {TEMA_ATUAL['COR_FUNDO']};
                padding: 6px;
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                border-radius: 4px;
                font-size: 10px;
                font-family: 'Courier New', monospace;
                min-height: 50px;
                max-height: 80px;
            }}
        """)
        self.preview_mapeamentos.setWordWrap(True)
        import_layout.addWidget(self.preview_mapeamentos)
        
        layout.addWidget(import_frame)
        
    def criar_botoes_acao(self, layout):
        # Frame dos botões
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(0, 12, 0, 0)
        buttons_layout.setSpacing(12)
        
        # Informações de alterações
        self.info_alteracoes = QLabel("Nenhuma alteração realizada")
        self.info_alteracoes.setStyleSheet(f"""
            color: {TEMA_ATUAL['COR_TEXTO']};
            font-size: 12px;
            font-style: italic;
        """)
        buttons_layout.addWidget(self.info_alteracoes)
        
        buttons_layout.addStretch()
        
        # Botão Cancelar
        btn_cancelar = QPushButton("❌ Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_cancelar.setStyleSheet(f"""
            QPushButton {{
                background-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                color: {TEMA_ATUAL['COR_TEXTO']};
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {TEMA_ATUAL['COR_DESTAQUE']};
                color: white;
            }}
        """)
        buttons_layout.addWidget(btn_cancelar)
        
        # Botão Gerar CNAB sem Juros
        self.btn_gerar_cnab_sem_juros = QPushButton("🔄 Gerar CNAB sem Juros")
        self.btn_gerar_cnab_sem_juros.clicked.connect(self.gerar_cnab_sem_juros)
        self.btn_gerar_cnab_sem_juros.setStyleSheet(f"""
            QPushButton {{
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 140px;
            }}
            QPushButton:hover {{
                background-color: #219a52;
            }}
        """)
        buttons_layout.addWidget(self.btn_gerar_cnab_sem_juros)
        
        # Botão Salvar
        self.btn_salvar = QPushButton("💾 Salvar Alterações")
        self.btn_salvar.clicked.connect(self.salvar_alteracoes)
        self.btn_salvar.setEnabled(False)
        self.btn_salvar.setStyleSheet(f"""
            QPushButton {{
                background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {TEMA_ATUAL['COR_BOTAO_HOVER']};
            }}
            QPushButton:disabled {{
                background-color: #A0AEC0;
                color: #EDF2F7;
            }}
        """)
        buttons_layout.addWidget(self.btn_salvar)
        
        layout.addWidget(buttons_frame)
        
    def aplicar_estilo(self):
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {TEMA_ATUAL['COR_FUNDO']};
                color: {TEMA_ATUAL['COR_TEXTO']};
            }}
        """)
        
    def carregar_dados(self):
        """Carrega os dados na tabela"""
        self.tabela_edicao.setRowCount(len(self.dados_editados))
        
        for i, detalhe in enumerate(self.dados_editados):
            # Sequencial
            item_seq = QTableWidgetItem(str(i + 1))
            item_seq.setFlags(item_seq.flags() & ~Qt.ItemIsEditable)
            item_seq.setTextAlignment(Qt.AlignCenter)
            self.tabela_edicao.setItem(i, 0, item_seq)
            
            # Nosso Número (editável)
            item_nosso = QTableWidgetItem(str(detalhe.get('nosso_numero', '')))
            item_nosso.setData(Qt.UserRole, 'nosso_numero')
            self.tabela_edicao.setItem(i, 1, item_nosso)
            
            # Código Empresa (editável)
            item_codigo = QTableWidgetItem(str(detalhe.get('codigo_empresa', '')))
            item_codigo.setData(Qt.UserRole, 'codigo_empresa')
            self.tabela_edicao.setItem(i, 2, item_codigo)
            
            # Seu Número (editável - mostrar apenas parte antes da barra)
            seu_numero_completo = str(detalhe.get('seu_numero', ''))
            # Se tem barra, mostrar apenas a parte antes da barra
            if '/' in seu_numero_completo:
                seu_numero_exibir = seu_numero_completo.split('/')[0]
            else:
                seu_numero_exibir = seu_numero_completo
            item_seu = QTableWidgetItem(seu_numero_exibir)
            item_seu.setData(Qt.UserRole, 'seu_numero')
            self.tabela_edicao.setItem(i, 3, item_seu)
            
            # Valor (apenas visualização)
            valor = detalhe.get('valor_titulo', 0)
            if isinstance(valor, (int, float)):
                valor_formatado = f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
            else:
                valor_formatado = str(valor)
            item_valor = QTableWidgetItem(valor_formatado)
            item_valor.setFlags(item_valor.flags() & ~Qt.ItemIsEditable)
            item_valor.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.tabela_edicao.setItem(i, 4, item_valor)
            
            # Vencimento (apenas visualização)
            item_venc = QTableWidgetItem(str(detalhe.get('data_vencimento', '')))
            item_venc.setFlags(item_venc.flags() & ~Qt.ItemIsEditable)
            item_venc.setTextAlignment(Qt.AlignCenter)
            self.tabela_edicao.setItem(i, 5, item_venc)
        
        # Ajustar largura das colunas
        self.tabela_edicao.resizeColumnsToContents()
        
    def filtrar_dados(self):
        """Filtra os dados baseado nos filtros"""
        filtro_nosso = self.filtro_nosso_numero.text().lower()
        filtro_codigo = self.filtro_codigo_empresa.text().lower()
        filtro_seu = self.filtro_seu_numero.text().lower()
        
        for i in range(self.tabela_edicao.rowCount()):
            mostrar_linha = True
            
            if filtro_nosso:
                item_nosso = self.tabela_edicao.item(i, 1)
                if item_nosso and filtro_nosso not in item_nosso.text().lower():
                    mostrar_linha = False
            
            if filtro_codigo and mostrar_linha:
                item_codigo = self.tabela_edicao.item(i, 2)
                if item_codigo and filtro_codigo not in item_codigo.text().lower():
                    mostrar_linha = False
            
            if filtro_seu and mostrar_linha:
                item_seu = self.tabela_edicao.item(i, 3)
                if item_seu and filtro_seu not in item_seu.text().lower():
                    mostrar_linha = False
            
            self.tabela_edicao.setRowHidden(i, not mostrar_linha)
    
    def limpar_filtros(self):
        """Limpa todos os filtros"""
        self.filtro_nosso_numero.clear()
        self.filtro_codigo_empresa.clear()
        self.filtro_seu_numero.clear()
        
        # Mostrar todas as linhas
        for i in range(self.tabela_edicao.rowCount()):
            self.tabela_edicao.setRowHidden(i, False)
    
    def item_editado(self, item):
        """Chamado quando um item da tabela é editado"""
        if not item:
            return
            
        linha = item.row()
        campo = item.data(Qt.UserRole)
        novo_valor = item.text().strip()
        
        if campo in ['nosso_numero', 'codigo_empresa', 'seu_numero']:
            # Validar o valor
            if campo == 'nosso_numero' and novo_valor:
                # Validar nosso número (alfanumérico, até 12 caracteres)
                if len(novo_valor) > 12 or not novo_valor.replace(' ', '').isalnum():
                    QMessageBox.warning(self, "Valor Inválido", 
                        "Nosso Número deve conter apenas letras e números e ter no máximo 12 caracteres.")
                    # Restaurar valor anterior
                    item.setText(str(self.dados_editados[linha].get(campo, '')))
                    return
            
            elif campo == 'codigo_empresa' and novo_valor:
                # Validar código da empresa (alfanumérico, até 17 caracteres)
                if len(novo_valor) > 17:
                    QMessageBox.warning(self, "Valor Inválido", 
                        "Código da Empresa deve ter no máximo 17 caracteres.")
                    # Restaurar valor anterior
                    item.setText(str(self.dados_editados[linha].get(campo, '')))
                    return
            
            elif campo == 'seu_numero':
                # Para Seu Número, aceitar qualquer valor e remover barra automaticamente
                if '/' in novo_valor:
                    # Remover automaticamente a barra e tudo depois dela
                    novo_valor = novo_valor.split('/')[0]
                    item.setText(novo_valor)
                
                # Validar tamanho
                if len(novo_valor) > 10:
                    QMessageBox.warning(self, "Valor Inválido", 
                        "O Seu Número deve ter no máximo 10 caracteres.")
                    # Restaurar valor anterior
                    valor_original = str(self.dados_editados[linha].get(campo, ''))
                    # Se valor original tem barra, usar só a parte antes da barra
                    if '/' in valor_original:
                        valor_original = valor_original.split('/')[0]
                    item.setText(valor_original)
                    return
            
            # Aplicar alteração
            self.dados_editados[linha][campo] = novo_valor
            self.dados_editados[linha]['_alterado'] = True
            self.alteracoes_realizadas = True
            
            # Atualizar interface
            self.atualizar_info_alteracoes()
            self.btn_salvar.setEnabled(True)
            
            # Destacar linha alterada
            for col in range(self.tabela_edicao.columnCount()):
                item_col = self.tabela_edicao.item(linha, col)
                if item_col:
                    item_col.setBackground(QColor(TEMA_ATUAL['COR_PRIMARIA']).lighter(180))
    
    def aplicar_nosso_numero_lote(self):
        """Aplica novo nosso número a todos os registros visíveis"""
        novo_valor = self.novo_nosso_numero.text().strip()
        
        if not novo_valor:
            QMessageBox.warning(self, "Valor Inválido", "Digite um valor para o Nosso Número.")
            return
        
        # Validar
        if len(novo_valor) > 12 or not novo_valor.replace(' ', '').isalnum():
            QMessageBox.warning(self, "Valor Inválido", 
                "Nosso Número deve conter apenas letras e números e ter no máximo 12 caracteres.")
            return
        
        # Confirmar ação
        registros_visiveis = sum(1 for i in range(self.tabela_edicao.rowCount()) 
                                if not self.tabela_edicao.isRowHidden(i))
        
        resposta = QMessageBox.question(self, "Confirmar Alteração",
            f"Deseja aplicar o Nosso Número '{novo_valor}' a {registros_visiveis} registro(s) visível(eis)?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if resposta != QMessageBox.Yes:
            return
        
        # Aplicar alteração
        alterados = 0
        for i in range(self.tabela_edicao.rowCount()):
            if not self.tabela_edicao.isRowHidden(i):
                # Atualizar dados
                self.dados_editados[i]['nosso_numero'] = novo_valor
                self.dados_editados[i]['_alterado'] = True
                
                # Atualizar tabela
                item = self.tabela_edicao.item(i, 1)
                if item:
                    item.setText(novo_valor)
                    item.setBackground(QColor(TEMA_ATUAL['COR_PRIMARIA']).lighter(180))
                
                # Destacar linha
                for col in range(self.tabela_edicao.columnCount()):
                    item_col = self.tabela_edicao.item(i, col)
                    if item_col:
                        item_col.setBackground(QColor(TEMA_ATUAL['COR_PRIMARIA']).lighter(180))
                
                alterados += 1
        
        self.alteracoes_realizadas = True
        self.btn_salvar.setEnabled(True)
        self.atualizar_info_alteracoes()
        self.novo_nosso_numero.clear()
        
        QMessageBox.information(self, "Alteração Aplicada", 
            f"Nosso Número alterado em {alterados} registro(s).")
    
    def aplicar_codigo_empresa_lote(self):
        """Aplica novo código de empresa a todos os registros visíveis"""
        novo_valor = self.novo_codigo_empresa.text().strip()
        
        if not novo_valor:
            QMessageBox.warning(self, "Valor Inválido", "Digite um valor para o Código da Empresa.")
            return
        
        # Validar
        if len(novo_valor) > 17:
            QMessageBox.warning(self, "Valor Inválido", 
                "Código da Empresa deve ter no máximo 17 caracteres.")
            return
        
        # Confirmar ação
        registros_visiveis = sum(1 for i in range(self.tabela_edicao.rowCount()) 
                                if not self.tabela_edicao.isRowHidden(i))
        
        resposta = QMessageBox.question(self, "Confirmar Alteração",
            f"Deseja aplicar o Código da Empresa '{novo_valor}' a {registros_visiveis} registro(s) visível(eis)?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if resposta != QMessageBox.Yes:
            return
        
        # Aplicar alteração
        alterados = 0
        for i in range(self.tabela_edicao.rowCount()):
            if not self.tabela_edicao.isRowHidden(i):
                # Atualizar dados
                self.dados_editados[i]['codigo_empresa'] = novo_valor
                self.dados_editados[i]['_alterado'] = True
                
                # Atualizar tabela
                item = self.tabela_edicao.item(i, 2)
                if item:
                    item.setText(novo_valor)
                    item.setBackground(QColor(TEMA_ATUAL['COR_PRIMARIA']).lighter(180))
                
                # Destacar linha
                for col in range(self.tabela_edicao.columnCount()):
                    item_col = self.tabela_edicao.item(i, col)
                    if item_col:
                        item_col.setBackground(QColor(TEMA_ATUAL['COR_PRIMARIA']).lighter(180))
                
                alterados += 1
        
        self.alteracoes_realizadas = True
        self.btn_salvar.setEnabled(True)
        self.atualizar_info_alteracoes()
        self.novo_codigo_empresa.clear()
        
        QMessageBox.information(self, "Alteração Aplicada", 
            f"Código da Empresa alterado em {alterados} registro(s).")
    
    def aplicar_seu_numero_lote(self):
        """Aplica novo Seu Número removendo completamente a barra e dígitos à direita"""
        novo_valor = self.novo_seu_numero.text().strip()
        
        if not novo_valor:
            QMessageBox.warning(self, "Valor Inválido", "Digite um valor para o Seu Número.")
            return
        
        # Validar
        if len(novo_valor) > 10:
            QMessageBox.warning(self, "Valor Inválido", 
                "O Seu Número deve ter no máximo 10 caracteres.")
            return
        
        if '/' in novo_valor:
            QMessageBox.warning(self, "Valor Inválido", 
                "Digite apenas o novo valor. A barra e dígitos à direita serão removidos completamente.")
            return
        
        # Confirmar ação
        registros_visiveis = sum(1 for i in range(self.tabela_edicao.rowCount()) 
                                if not self.tabela_edicao.isRowHidden(i))
        
        resposta = QMessageBox.question(self, "Confirmar Alteração",
            f"Deseja aplicar '{novo_valor}' como Seu Número em {registros_visiveis} registro(s) visível(eis)?\n\n"
            "⚠️ ATENÇÃO: A barra (/) e os 3 dígitos à direita serão REMOVIDOS COMPLETAMENTE.\n"
            "O arquivo final conterá apenas o novo valor digitado.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if resposta != QMessageBox.Yes:
            return
        
        # Aplicar alteração
        alterados = 0
        for i in range(self.tabela_edicao.rowCount()):
            if not self.tabela_edicao.isRowHidden(i):
                # Usar apenas o novo valor (sem barra nem dígitos à direita)
                novo_valor_completo = novo_valor
                
                # Atualizar dados
                self.dados_editados[i]['seu_numero'] = novo_valor_completo
                self.dados_editados[i]['_alterado'] = True
                
                # Atualizar tabela
                item = self.tabela_edicao.item(i, 3)
                if item:
                    item.setText(novo_valor_completo)
                    item.setBackground(QColor(TEMA_ATUAL['COR_PRIMARIA']).lighter(180))
                
                # Destacar linha
                for col in range(self.tabela_edicao.columnCount()):
                    item_col = self.tabela_edicao.item(i, col)
                    if item_col:
                        item_col.setBackground(QColor(TEMA_ATUAL['COR_PRIMARIA']).lighter(180))
                
                alterados += 1
        
        self.alteracoes_realizadas = True
        self.btn_salvar.setEnabled(True)
        self.atualizar_info_alteracoes()
        self.novo_seu_numero.clear()
        
        QMessageBox.information(self, "Alteração Aplicada", 
            f"Seu Número alterado em {alterados} registro(s). Barra e dígitos à direita removidos.")
    
    def atualizar_info_alteracoes(self):
        """Atualiza as informações sobre alterações"""
        alterados = sum(1 for d in self.dados_editados if d.get('_alterado', False))
        
        if alterados > 0:
            self.info_alteracoes.setText(f"✏️ {alterados} registro(s) alterado(s)")
            self.info_alteracoes.setStyleSheet(f"""
                color: {TEMA_ATUAL['COR_PRIMARIA']};
                font-size: 12px;
                font-weight: bold;
            """)
        else:
            self.info_alteracoes.setText("Nenhuma alteração realizada")
            self.info_alteracoes.setStyleSheet(f"""
                color: {TEMA_ATUAL['COR_TEXTO']};
                font-size: 12px;
                font-style: italic;
            """)
    
    def salvar_alteracoes(self):
        """Salva as alterações realizadas"""
        if not self.alteracoes_realizadas:
            QMessageBox.information(self, "Nenhuma Alteração", 
                "Não há alterações para salvar.")
            return
        
        # Confirmar salvamento
        alterados = sum(1 for d in self.dados_editados if d.get('_alterado', False))
        resposta = QMessageBox.question(self, "Salvar Alterações",
            f"Deseja salvar as alterações realizadas em {alterados} registro(s)?\n\n"
            "Um novo arquivo CNAB será gerado com as modificações.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if resposta != QMessageBox.Yes:
            return
        
        try:
            # Aplicar alterações no processador
            for i, dados_editado in enumerate(self.dados_editados):
                if dados_editado.get('_alterado', False):
                    # Atualizar dados originais
                    self.processador.detalhes[i].update(dados_editado)
            
            # Gerar novo arquivo
            nome_arquivo = os.path.basename(self.processador.arquivo)
            nome_base = os.path.splitext(nome_arquivo)[0]
            
            options = QFileDialog.Options()
            caminho_novo, _ = QFileDialog.getSaveFileName(
                self, "Salvar Arquivo CNAB Editado", 
                f"{nome_base}_editado.TXT",
                "Arquivos CNAB (*.TXT);;Todos os Arquivos (*)", 
                options=options
            )
            
            if caminho_novo:
                # Usar método do processador para gerar novo arquivo
                sucesso, mensagem = self.processador.gerar_cnab_editado(caminho_novo)
                
                if sucesso:
                    QMessageBox.information(self, "Alterações Salvas",
                        f"As alterações foram salvas com sucesso!\n\n"
                        f"Arquivo gerado: {os.path.basename(caminho_novo)}\n"
                        f"Registros alterados: {alterados}")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Erro ao Salvar", 
                        f"Erro ao salvar as alterações:\n{mensagem}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", 
                f"Erro inesperado ao salvar alterações:\n{str(e)}")
    
    def gerar_cnab_sem_juros(self):
        """Gera arquivo CNAB sem juros aplicando as modificações do editor gráfico"""
        try:
            # Verificar se há dados para processar
            if not self.dados_editados:
                QMessageBox.warning(self, "Nenhum Dado", 
                    "Não há dados para processar.")
                return
            
            # Aplicar alterações temporariamente no processador
            alterados = sum(1 for d in self.dados_editados if d.get('_alterado', False))
            
            # Mostrar informações sobre o que será feito
            if alterados > 0:
                resposta = QMessageBox.question(self, "Gerar CNAB sem Juros",
                    f"🔄 GERAR CNAB SEM JUROS\n\n"
                    f"Esta operação irá:\n"
                    f"• Aplicar {alterados} modificação(ões) do editor gráfico\n"
                    f"• Zerar todos os valores de juros/multa\n"
                    f"• Gerar um novo arquivo CNAB\n\n"
                    f"Deseja continuar?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            else:
                resposta = QMessageBox.question(self, "Gerar CNAB sem Juros",
                    f"🔄 GERAR CNAB SEM JUROS\n\n"
                    f"Esta operação irá:\n"
                    f"• Zerar todos os valores de juros/multa\n"
                    f"• Gerar um novo arquivo CNAB\n\n"
                    f"Nenhuma modificação do editor será aplicada (não há alterações).\n\n"
                    f"Deseja continuar?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            
            if resposta != QMessageBox.Yes:
                return
            
            # Aplicar alterações temporariamente no processador
            dados_originais = []
            for i, dados_editado in enumerate(self.dados_editados):
                if dados_editado.get('_alterado', False):
                    # Salvar dados originais para restaurar depois
                    dados_originais.append((i, self.processador.detalhes[i].copy()))
                    # Aplicar alterações temporariamente
                    self.processador.detalhes[i].update(dados_editado)
            
            # Gerar nome do arquivo
            nome_arquivo = os.path.basename(self.processador.arquivo)
            nome_base = os.path.splitext(nome_arquivo)[0]
            
            if alterados > 0:
                nome_sugerido = f"{nome_base}_editado_sem_juros.TXT"
            else:
                nome_sugerido = f"{nome_base}_sem_juros.TXT"
            
            options = QFileDialog.Options()
            caminho_novo, _ = QFileDialog.getSaveFileName(
                self, "Salvar Arquivo CNAB sem Juros", 
                nome_sugerido,
                "Arquivos CNAB (*.TXT);;Todos os Arquivos (*)", 
                options=options
            )
            
            if caminho_novo:
                # Usar novo método do processador para gerar arquivo sem juros
                sucesso, mensagem = self.processador.gerar_cnab_editado_sem_juros(caminho_novo)
                
                # Restaurar dados originais
                for i, dados_original in dados_originais:
                    self.processador.detalhes[i] = dados_original
                
                if sucesso:
                    QMessageBox.information(self, "CNAB Gerado com Sucesso",
                        f"✅ {mensagem}\n\n"
                        f"📄 Arquivo: {os.path.basename(caminho_novo)}\n"
                        f"🔧 Modificações aplicadas: {alterados}\n"
                        f"💰 Juros/multa zerados em todos os registros")
                else:
                    QMessageBox.critical(self, "Erro ao Gerar CNAB", 
                        f"❌ {mensagem}")
            else:
                # Restaurar dados originais se cancelou
                for i, dados_original in dados_originais:
                    self.processador.detalhes[i] = dados_original
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", 
                f"Erro inesperado ao gerar CNAB sem juros:\n{str(e)}")
    
    def selecionar_planilha_mapeamento(self):
        """Seleciona planilha Excel com mapeamentos"""
        arquivo_excel, _ = QFileDialog.getOpenFileName(
            self, 
            "Selecionar Planilha de Mapeamentos", 
            "", 
            "Arquivos Excel (*.xlsx *.xls)"
        )
        
        if not arquivo_excel:
            return
        
        try:
            # Ler planilha
            import pandas as pd
            df_mapeamentos = pd.read_excel(arquivo_excel)
            
            # Determinar tipo de mapeamento baseado no combo
            tipo_selecionado = self.tipo_mapeamento.currentText()
            
            if "NOSSO_NUMERO" in tipo_selecionado:
                colunas_necessarias = ['NOSSO_NUMERO_ATUAL', 'NOSSO_NUMERO_CORRIGIDO']
                self.tipo_mapeamento_atual = 'nosso_numero'
            else:
                colunas_necessarias = ['SEU_NUMERO_COMPLETO_ATUAL', 'SEU_NUMERO_NOVO']
                self.tipo_mapeamento_atual = 'seu_numero'
            
            # Verificar colunas obrigatórias
            colunas_faltando = [col for col in colunas_necessarias if col not in df_mapeamentos.columns]
            
            if colunas_faltando:
                QMessageBox.warning(self, "Colunas Faltando", 
                    f"A planilha deve conter as colunas:\n{', '.join(colunas_necessarias)}\n\n"
                    f"Colunas faltando: {', '.join(colunas_faltando)}")
                return
            
            # Limpar dados vazios
            df_mapeamentos = df_mapeamentos.dropna(subset=colunas_necessarias)
            
            if df_mapeamentos.empty:
                QMessageBox.warning(self, "Planilha Vazia", 
                    "A planilha não contém dados válidos nas colunas necessárias.")
                return
            
            # Converter para string e remover espaços baseado no tipo
            if self.tipo_mapeamento_atual == 'nosso_numero':
                df_mapeamentos['NOSSO_NUMERO_ATUAL'] = df_mapeamentos['NOSSO_NUMERO_ATUAL'].astype(str).str.strip()
                df_mapeamentos['NOSSO_NUMERO_CORRIGIDO'] = df_mapeamentos['NOSSO_NUMERO_CORRIGIDO'].astype(str).str.strip()
            else:
                df_mapeamentos['SEU_NUMERO_COMPLETO_ATUAL'] = df_mapeamentos['SEU_NUMERO_COMPLETO_ATUAL'].astype(str).str.strip()
                df_mapeamentos['SEU_NUMERO_NOVO'] = df_mapeamentos['SEU_NUMERO_NOVO'].astype(str).str.strip()
            
            # Armazenar dados
            self.df_mapeamentos = df_mapeamentos
            self.arquivo_planilha = arquivo_excel
            
            # Atualizar interface
            nome_arquivo = os.path.basename(arquivo_excel)
            self.planilha_selecionada.setText(f"📄 {nome_arquivo} ({len(df_mapeamentos)} mapeamentos)")
            
            # Gerar preview
            self.gerar_preview_mapeamentos()
            
            # Habilitar botão de aplicar
            self.btn_aplicar_mapeamentos.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro ao Ler Planilha", 
                f"Erro ao processar planilha:\n{str(e)}")
    
    def gerar_preview_mapeamentos(self):
        """Gera preview dos mapeamentos da planilha"""
        if not hasattr(self, 'df_mapeamentos'):
            return
        
        df = self.df_mapeamentos
        
        # Contar quantos registros serão afetados baseado no tipo
        if self.tipo_mapeamento_atual == 'nosso_numero':
            valores_atuais = set(df['NOSSO_NUMERO_ATUAL'].astype(str))
            campo_cnab = 'nosso_numero'
            nome_campo = 'Nosso Número'
            
            registros_encontrados = 0
            for detalhe in self.dados_editados:
                valor_cnab = str(detalhe.get(campo_cnab, '')).strip()
                if valor_cnab in valores_atuais:
                    registros_encontrados += 1
        else:
            # Para SEU_NUMERO, comparar o valor completo (com barra e dígitos)
            valores_atuais = set(df['SEU_NUMERO_COMPLETO_ATUAL'].astype(str))
            campo_cnab = 'seu_numero'
            nome_campo = 'Seu Número'
            
            registros_encontrados = 0
            for detalhe in self.dados_editados:
                valor_cnab = str(detalhe.get(campo_cnab, '')).strip()
                # Comparar o valor completo
                if valor_cnab in valores_atuais:
                    registros_encontrados += 1
        
        # Gerar preview text
        preview_lines = []
        preview_lines.append(f"📊 PREVIEW DOS MAPEAMENTOS - {nome_campo.upper()}:")
        preview_lines.append(f"📄 Total de mapeamentos na planilha: {len(df)}")
        preview_lines.append(f"🎯 Registros CNAB que serão afetados: {registros_encontrados}")
        preview_lines.append("")
        preview_lines.append("📋 Primeiros mapeamentos:")
        
        # Mostrar primeiros 5 mapeamentos
        for i, (_, row) in enumerate(df.head(5).iterrows()):
            if self.tipo_mapeamento_atual == 'nosso_numero':
                atual = row['NOSSO_NUMERO_ATUAL']
                corrigido = row['NOSSO_NUMERO_CORRIGIDO']
                preview_lines.append(f"  {atual} → {corrigido}")
            else:
                atual = row['SEU_NUMERO_COMPLETO_ATUAL']
                novo = row['SEU_NUMERO_NOVO']
                
                # Para Seu Número, mostrar como ficará após o mapeamento
                if '/' in atual:
                    parte_depois_barra = atual.split('/', 1)[1]
                    resultado_mapeamento = f"{novo}/{parte_depois_barra}"
                else:
                    resultado_mapeamento = novo
                
                preview_lines.append(f"  {atual} → {resultado_mapeamento}")
                continue
        
        if len(df) > 5:
            preview_lines.append(f"  ... e mais {len(df) - 5} mapeamentos")
        
        if self.tipo_mapeamento_atual == 'seu_numero':
            preview_lines.append("")
            preview_lines.append("ℹ️ Para SEU_NUMERO: a parte antes da barra será substituída, preservando /dígitos")
            preview_lines.append("⚠️ A barra e dígitos serão removidos apenas no arquivo CNAB final")
        
        preview_text = "\n".join(preview_lines)
        self.preview_mapeamentos.setText(preview_text)
    
    def aplicar_mapeamentos_planilha(self):
        """Aplica os mapeamentos da planilha aos dados"""
        if not hasattr(self, 'df_mapeamentos'):
            QMessageBox.warning(self, "Nenhuma Planilha", 
                "Selecione uma planilha de mapeamentos primeiro.")
            return
        
        # Confirmar operação
        df = self.df_mapeamentos
        tipo_campo = "Nosso Número" if self.tipo_mapeamento_atual == 'nosso_numero' else "Seu Número"
        
        resposta = QMessageBox.question(self, "Confirmar Mapeamentos",
            f"Deseja aplicar {len(df)} mapeamento(s) da planilha para {tipo_campo}?\n\n"
            f"Esta operação irá substituir os valores conforme a planilha.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if resposta != QMessageBox.Yes:
            return
        
        try:
            # Criar dicionário de mapeamentos baseado no tipo
            mapeamentos = {}
            for _, row in df.iterrows():
                if self.tipo_mapeamento_atual == 'nosso_numero':
                    atual = str(row['NOSSO_NUMERO_ATUAL']).strip()
                    corrigido = str(row['NOSSO_NUMERO_CORRIGIDO']).strip()
                    
                    # Validar nosso número corrigido
                    if len(corrigido) > 12 or not corrigido.replace(' ', '').isalnum():
                        QMessageBox.warning(self, "Valor Inválido", 
                            f"Nosso Número corrigido inválido: '{corrigido}'\n"
                            "Deve conter apenas letras e números e ter no máximo 12 caracteres.")
                        return
                    
                    mapeamentos[atual] = corrigido
                else:
                    # Para SEU_NUMERO, usar o valor completo como chave e o novo valor
                    valor_completo_atual = str(row['SEU_NUMERO_COMPLETO_ATUAL']).strip()
                    valor_novo = str(row['SEU_NUMERO_NOVO']).strip()
                    
                    # Validar valor novo (aceita alfanumérico como 49635C)
                    if len(valor_novo) > 10 or not valor_novo.replace(' ', '').isalnum():
                        QMessageBox.warning(self, "Valor Inválido", 
                            f"Seu Número novo inválido: '{valor_novo}'\n"
                            "Deve conter apenas letras e números e ter no máximo 10 caracteres.\n"
                            "Exemplos válidos: 49635, 49635C, ABC123")
                        return
                    
                    mapeamentos[valor_completo_atual] = valor_novo
            
            # Debug: mostrar mapeamentos carregados
            if self.tipo_mapeamento_atual == 'seu_numero':
                print(f"DEBUG: Mapeamentos carregados: {list(mapeamentos.keys())[:10]}")
            
            # Aplicar mapeamentos
            alterados = 0
            debug_info = []  # Para debug
            
            for i, detalhe in enumerate(self.dados_editados):
                if self.tipo_mapeamento_atual == 'nosso_numero':
                    valor_atual = str(detalhe.get('nosso_numero', '')).strip()
                    coluna_tabela = 1
                    
                    if valor_atual in mapeamentos:
                        novo_valor = mapeamentos[valor_atual]
                    else:
                        continue  # Não há mapeamento para este registro
                else:
                    # Para SEU_NUMERO, comparar o valor completo (com barra e dígitos)
                    valor_seu_numero = str(detalhe.get('seu_numero', '')).strip()
                    coluna_tabela = 3
                    
                    # Debug: adicionar informações
                    debug_info.append(f"Registro {i+1}: '{valor_seu_numero}' -> {'SIM' if valor_seu_numero in mapeamentos else 'NÃO'}")
                    
                    if valor_seu_numero in mapeamentos:
                        # Preservar a estrutura: substituir apenas a parte antes da barra
                        valor_novo_planilha = mapeamentos[valor_seu_numero]
                        
                        if '/' in valor_seu_numero:
                            # Manter a barra e dígitos originais
                            parte_depois_barra = valor_seu_numero.split('/', 1)[1]
                            novo_valor = f"{valor_novo_planilha}/{parte_depois_barra}"
                        else:
                            # Se não tem barra, usar apenas o novo valor
                            novo_valor = valor_novo_planilha
                    else:
                        continue  # Não há mapeamento para este registro
                
                # Atualizar dados
                campo = 'nosso_numero' if self.tipo_mapeamento_atual == 'nosso_numero' else 'seu_numero'
                self.dados_editados[i][campo] = novo_valor
                self.dados_editados[i]['_alterado'] = True
                
                # Atualizar tabela
                item = self.tabela_edicao.item(i, coluna_tabela)
                if item:
                    item.setText(novo_valor)
                    item.setBackground(QColor(TEMA_ATUAL['COR_PRIMARIA']).lighter(180))
                
                # Destacar linha
                for col in range(self.tabela_edicao.columnCount()):
                    item_col = self.tabela_edicao.item(i, col)
                    if item_col:
                        item_col.setBackground(QColor(TEMA_ATUAL['COR_PRIMARIA']).lighter(180))
                
                alterados += 1
            
            # Atualizar interface
            self.alteracoes_realizadas = True
            self.btn_salvar.setEnabled(True)
            self.atualizar_info_alteracoes()
            
            # Mostrar resultado com debug para SEU_NUMERO
            if self.tipo_mapeamento_atual == 'seu_numero' and alterados == 0:
                debug_text = "\n".join(debug_info[:10])  # Mostrar primeiros 10
                QMessageBox.information(self, "Debug - Mapeamentos", 
                    f"🔍 DEBUG - Nenhum mapeamento aplicado\n\n"
                    f"📊 {alterados} registro(s) foram alterados\n"
                    f"📄 {len(df)} mapeamento(s) processados\n"
                    f"🎯 Taxa de aplicação: {(alterados/len(df)*100):.1f}%\n\n"
                    f"🔍 Primeiros registros analisados:\n{debug_text}")
            else:
                QMessageBox.information(self, "Mapeamentos Aplicados", 
                    f"✅ Mapeamentos de {tipo_campo} aplicados com sucesso!\n\n"
                    f"📊 {alterados} registro(s) foram alterados\n"
                    f"📄 {len(df)} mapeamento(s) processados\n"
                    f"🎯 Taxa de aplicação: {(alterados/len(df)*100):.1f}%")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", 
                f"Erro ao aplicar mapeamentos:\n{str(e)}")
    
    def atualizar_preview_tipo_mapeamento(self):
        """Atualiza o preview quando o tipo de mapeamento é alterado"""
        # Limpar planilha selecionada se houver
        if hasattr(self, 'df_mapeamentos'):
            delattr(self, 'df_mapeamentos')
        
        # Resetar interface
        self.planilha_selecionada.setText("Nenhuma planilha selecionada")
        self.preview_mapeamentos.setText("Preview aparecerá após selecionar planilha")
        self.btn_aplicar_mapeamentos.setEnabled(False)


class CNABBradescoGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurações de janela
        self.setWindowTitle("Leitor CNAB 400 - Bradesco")
        self.setMinimumSize(900, 650)
        self.setWindowIcon(QIcon("icon.png"))  # Substituir pelo caminho do ícone real, se disponível
        
        # Variáveis de instância
        self.arquivo_atual = None
        self.df = None
        self.central_widget = None
        self.tabela = None
        self.progresso = None
        self.status_bar = None
        self.tabs = None
        
        # Inicializar o locale para formatação monetária
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        except locale.Error:
            try:
                # Tentar alternativa para Windows
                locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
            except locale.Error:
                print("Aviso: Não foi possível configurar o locale para português brasileiro.")
        
        # Configurar a interface
        self.setStyleSheet(f"background-color: {TEMA_ATUAL['COR_FUNDO']}; color: {TEMA_ATUAL['COR_TEXTO']};")
        self.setup_ui()
        
        # Mensagem inicial
        print("Iniciando interface gráfica...")
        
    def setup_ui(self):
        # Widget central se ainda não existir
        if not hasattr(self, 'central_widget') or self.central_widget is None:
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)
            
            # Layout principal
            self.main_layout = QVBoxLayout(self.central_widget)
            self.main_layout.setContentsMargins(12, 12, 12, 12)
            self.main_layout.setSpacing(8)
            
            # Cabeçalho
            self._criar_cabecalho(self.main_layout)
            
            # Área de controles
            self._criar_area_controles(self.main_layout)
            
            # Abas para detalhes e resumo
            self.tabs = QTabWidget()
            
            # Aba de detalhes
            self.tab_detalhes = QWidget()
            self.layout_detalhes = QVBoxLayout(self.tab_detalhes)
            self.layout_detalhes.setContentsMargins(8, 8, 8, 8)
            self.layout_detalhes.setSpacing(6)
            self._criar_aba_detalhes(self.layout_detalhes)
            
            # Aba de resumo
            self.tab_resumo = QWidget()
            self.layout_resumo = QVBoxLayout(self.tab_resumo)
            self.layout_resumo.setContentsMargins(8, 8, 8, 8)
            self.layout_resumo.setSpacing(6)
            self._criar_aba_resumo(self.layout_resumo)
            
            # Adicionar abas
            self.tabs.addTab(self.tab_detalhes, "Detalhes dos Títulos")
            self.tabs.addTab(self.tab_resumo, "Resumo")
            
            self.main_layout.addWidget(self.tabs, 1)
            
            # Barra de status
            self.status_bar = QStatusBar()
            self.setStatusBar(self.status_bar)
            self.status_bar.showMessage("Pronto para processar arquivos CNAB 400 do Bradesco")
            
            # Barra de progresso
            self._criar_barra_progresso(self.main_layout)
        else:
            # Verificar se os componentes principais existem e inicializá-los se necessário
            if self.tabs is None:
                self.tabs = QTabWidget()
                
                # Aba de detalhes
                self.tab_detalhes = QWidget()
                self.layout_detalhes = QVBoxLayout(self.tab_detalhes)
                self.layout_detalhes.setContentsMargins(8, 8, 8, 8)
                self.layout_detalhes.setSpacing(6)
                self._criar_aba_detalhes(self.layout_detalhes)
                
                # Aba de resumo
                self.tab_resumo = QWidget()
                self.layout_resumo = QVBoxLayout(self.tab_resumo)
                self.layout_resumo.setContentsMargins(8, 8, 8, 8)
                self.layout_resumo.setSpacing(6)
                self._criar_aba_resumo(self.layout_resumo)
                
                # Adicionar abas
                self.tabs.addTab(self.tab_detalhes, "Detalhes dos Títulos")
                self.tabs.addTab(self.tab_resumo, "Resumo")
                
                self.main_layout.addWidget(self.tabs, 1)
            
            if self.status_bar is None:
                self.status_bar = QStatusBar()
                self.setStatusBar(self.status_bar)
                self.status_bar.showMessage("Pronto para processar arquivos CNAB 400 do Bradesco")
        
        # Atualizar os estilos
        self.atualizar_estilos()
        
    def atualizar_estilos(self):
        """Atualiza todos os estilos baseados no tema atual"""
        # Estilo geral
        self.setStyleSheet(f"background-color: {TEMA_ATUAL['COR_FUNDO']}; color: {TEMA_ATUAL['COR_TEXTO']};")
        
        # Atualizar frames
        for frame in self.findChildren(QFrame):
            if frame.objectName() == "cabecalho":
                frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: {TEMA_ATUAL['COR_CABECALHO']};
                        border-radius: 8px;
                        margin: 0px;
                        padding: 0px;
                    }}
                """)
            else:
                frame.setStyleSheet(f"""
                    QFrame {{
                        background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                        border-radius: 6px;
                    }}
                """)
        
        # Tabs
        if self.tabs is not None:
            self.tabs.setStyleSheet(f"""
                QTabWidget::pane {{ 
                    border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                    border-radius: 8px;
                    background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                    top: -1px;
                }}
                QTabBar::tab {{
                    background-color: {TEMA_ATUAL['COR_FUNDO']};
                    color: {TEMA_ATUAL['COR_TEXTO']};
                    border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                    border-bottom: none;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                    padding: 10px 16px;
                    min-width: 140px;
                    font-weight: bold;
                    font-size: 13px;
                    margin-right: 2px;
                }}
                QTabBar::tab:selected {{
                    background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                    border-bottom: 2px solid {TEMA_ATUAL['COR_PRIMARIA']};
                }}
                QTabBar::tab:!selected {{
                    margin-top: 3px;
                }}
                QTabBar::tab:hover {{
                    background-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                }}
            """)
        
        # Status bar
        if self.status_bar is not None:
            self.status_bar.setStyleSheet(f"""
                QStatusBar {{
                    background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                    color: {TEMA_ATUAL['COR_TEXTO']};
                    border-top: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                    padding: 4px;
                    font-size: 12px;
                }}
            """)
        
        # Atualizar tabela
        if hasattr(self, 'tabela') and self.tabela is not None:
            self.tabela.setStyleSheet(f"""
                QTableWidget {{
                    background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                    color: {TEMA_ATUAL['COR_TEXTO']};
                    gridline-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                    border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                    border-radius: 8px;
                    padding: 2px;
                }}
                QTableWidget::item {{
                    padding: 8px;
                    border-bottom: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                }}
                QTableWidget::item:selected {{
                    background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                    color: white;
                }}
                QHeaderView::section {{
                    background-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                    color: {TEMA_ATUAL['COR_TEXTO']};
                    padding: 10px;
                    border: none;
                    font-weight: bold;
                    text-align: center;
                }}
                QTableWidget QTableCornerButton::section {{
                    background-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                    border: none;
                }}
            """)
        
        # Atualizar grupos (QGroupBox)
        for group in self.findChildren(QGroupBox):
            group.setStyleSheet(f"""
                QGroupBox {{
                    font-size: 14px;
                    font-weight: bold;
                    border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                    border-radius: 8px;
                    margin-top: 16px;
                    background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                    color: {TEMA_ATUAL['COR_TEXTO']};
                    padding: 8px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 12px;
                    padding: 0 5px 0 5px;
                    color: {TEMA_ATUAL['COR_PRIMARIA']};
                }}
            """)
        
        # Atualizar scroll areas
        for scroll in self.findChildren(QScrollArea):
            scroll.setStyleSheet(f"""
                QScrollArea {{
                    background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                    border-radius: 8px;
                    border: none;
                }}
                QScrollBar:vertical {{
                    border: none;
                    background: {TEMA_ATUAL['COR_TABELA_HEADER']};
                    width: 10px;
                    margin: 0px;
                    border-radius: 5px;
                }}
                QScrollBar::handle:vertical {{
                    background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                    border-radius: 5px;
                    min-height: 30px;
                }}
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                    height: 0px;
                }}
            """)
        
        # Atualizar o progresso
        if hasattr(self, 'progresso') and self.progresso is not None:
            self.progresso.setStyleSheet(f"""
                QProgressBar {{
                    background-color: {TEMA_ATUAL['COR_FUNDO']};
                    color: {TEMA_ATUAL['COR_TEXTO']};
                    border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                    border-radius: 5px;
                    text-align: center;
                    height: 22px;
                    min-height: 22px;
                }}
                QProgressBar::chunk {{
                    background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                    border-radius: 4px;
                }}
            """)
        
        # Forçar repintura da interface
        self.repaint()

    def _criar_cabecalho(self, layout):
        # Container do cabeçalho
        cabecalho = QFrame()
        cabecalho.setObjectName("cabecalho")
        cabecalho.setFixedHeight(70)
        cabecalho.setStyleSheet(f"""
            QFrame {{
                background-color: {TEMA_ATUAL['COR_CABECALHO']};
                border-radius: 8px;
                margin: 0px;
                padding: 0px;
            }}
        """)
        
        # Layout principal do cabeçalho
        layout_cabecalho = QHBoxLayout(cabecalho)
        layout_cabecalho.setContentsMargins(20, 0, 20, 0)
        layout_cabecalho.setSpacing(15)
        
        # Container do ícone
        icon_container = QFrame()
        icon_container.setFixedSize(45, 45)
        icon_container.setStyleSheet(f"""
            QFrame {{
                background-color: {TEMA_ATUAL['COR_DESTAQUE']};
                border-radius: 22px;
                border: 2px solid white;
                margin: 0px;
                padding: 0px;
            }}
        """)
        
        # Layout do ícone
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setSpacing(0)
        
        # Número do banco
        icon_label = QLabel("237")
        icon_label.setStyleSheet("""
            color: white; 
            font-size: 16px; 
            font-weight: bold; 
            font-family: 'Segoe UI';
            margin: 0px;
            padding: 0px;
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        
        # Container para título e subtítulo
        titulo_widget = QWidget()
        titulo_container = QVBoxLayout(titulo_widget)
        titulo_container.setContentsMargins(0, 12, 0, 12)
        titulo_container.setSpacing(4)
        
        # Título
        lbl_titulo = QLabel("CNAB 400 - Bradesco")
        lbl_titulo.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            font-family: 'Segoe UI';
        """)
        
        # Subtítulo
        lbl_subtitulo = QLabel("Sistema de Leitura de Arquivos de Retorno")
        lbl_subtitulo.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            font-size: 12px;
            font-family: 'Segoe UI';
        """)
        
        # Adiciona título e subtítulo ao container
        titulo_container.addWidget(lbl_titulo)
        titulo_container.addWidget(lbl_subtitulo)
        
        # Adiciona os elementos ao layout do cabeçalho
        layout_cabecalho.addWidget(icon_container)
        layout_cabecalho.addWidget(titulo_widget, 1)
        
        # Adiciona o cabeçalho ao layout principal
        layout.addWidget(cabecalho)
        
    def _criar_area_controles(self, layout):
        # Container para a área de controles
        controles_frame = QFrame()
        controles_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                border-radius: 8px;
                margin-top: 8px;
                margin-bottom: 8px;
            }}
        """)
        
        layout_controles = QVBoxLayout(controles_frame)
        layout_controles.setContentsMargins(16, 16, 16, 16)
        layout_controles.setSpacing(12)
        
        # Container para a seleção de arquivo com visual aprimorado
        arquivo_container = QHBoxLayout()
        arquivo_container.setSpacing(10)
        
        # Ícone para o arquivo
        icon_arquivo = QLabel("📄")
        icon_arquivo.setStyleSheet(f"""
            font-size: 20px;
            color: {TEMA_ATUAL['COR_PRIMARIA']};
            padding-right: 5px;
        """)
        arquivo_container.addWidget(icon_arquivo)
        
        # Label para mostrar o arquivo selecionado
        self.lbl_arquivo = QLabel("Arquivo: Nenhum arquivo selecionado")
        self.lbl_arquivo.setStyleSheet(f"""
            color: {TEMA_ATUAL['COR_TEXTO']};
            background-color: {TEMA_ATUAL['COR_FUNDO']};
            padding: 8px;
            border-radius: 6px;
            border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
            font-family: 'Segoe UI';
            font-size: 13px;
        """)
        arquivo_container.addWidget(self.lbl_arquivo, 1)
        
        # Botão para selecionar arquivo
        btn_selecionar = EstiloBotao("Selecionar Arquivo", True)
        btn_selecionar.clicked.connect(self.selecionar_arquivo)
        btn_selecionar.setMinimumWidth(150)
        arquivo_container.addWidget(btn_selecionar)
        
        layout_controles.addLayout(arquivo_container)
        
        # Container para botões de ação
        botoes_container = QHBoxLayout()
        botoes_container.setSpacing(10)
        
        # Botão para processar arquivo
        self.btn_processar = EstiloBotao("Processar Arquivo", True)
        self.btn_processar.clicked.connect(self.processar_arquivo)
        self.btn_processar.setEnabled(False)
        self.btn_processar.setMinimumWidth(150)
        botoes_container.addWidget(self.btn_processar)
        
        # Botão para exportar para CSV
        self.btn_exportar_csv = EstiloBotao("Exportar CSV", False)
        self.btn_exportar_csv.clicked.connect(self.exportar_csv)
        self.btn_exportar_csv.setEnabled(False)
        self.btn_exportar_csv.setMinimumWidth(130)
        botoes_container.addWidget(self.btn_exportar_csv)
        
        # Botão para exportar para Excel
        self.btn_exportar_excel = EstiloBotao("Exportar Excel", False)
        self.btn_exportar_excel.clicked.connect(self.exportar_excel)
        self.btn_exportar_excel.setEnabled(False)
        self.btn_exportar_excel.setMinimumWidth(130)
        botoes_container.addWidget(self.btn_exportar_excel)
        
        # Botão para gerar CNAB sem juros
        self.btn_gerar_cnab = EstiloBotao("Gerar CNAB sem Juros", False)
        self.btn_gerar_cnab.clicked.connect(self.gerar_cnab_retorno)
        self.btn_gerar_cnab.setEnabled(False)
        self.btn_gerar_cnab.setMinimumWidth(170)
        botoes_container.addWidget(self.btn_gerar_cnab)
        
        layout_controles.addLayout(botoes_container)
        
        # Segunda linha de botões para conversão
        botoes_container2 = QHBoxLayout()
        botoes_container2.setSpacing(10)
        
        # Botão para Excel para CNAB
        self.btn_excel_para_cnab = QPushButton("Excel → CNAB")
        self.btn_excel_para_cnab.clicked.connect(self.excel_para_cnab)
        self.btn_excel_para_cnab.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {{
                background-color: #005a9a;
            }}
        """)
        botoes_container2.addWidget(self.btn_excel_para_cnab)
        
        # Botão para Editor Interativo
        self.btn_editor_interativo = QPushButton("📝 Editor Interativo")
        self.btn_editor_interativo.clicked.connect(self.editor_interativo)
        self.btn_editor_interativo.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        botoes_container2.addWidget(self.btn_editor_interativo)
        
        # Botão para Editor Gráfico
        self.btn_editor_grafico = QPushButton("✏️ Editor Gráfico")
        self.btn_editor_grafico.clicked.connect(self.editor_grafico)
        self.btn_editor_grafico.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        botoes_container2.addWidget(self.btn_editor_grafico)
        
        layout_controles.addLayout(botoes_container2)
        
        layout.addWidget(controles_frame)
        
    def _criar_barra_progresso(self, layout):
        # Frame para a barra de progresso
        progresso_frame = QFrame()
        progresso_frame.setMinimumHeight(40)
        progresso_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                border-radius: 8px;
                margin-top: 8px;
                margin-bottom: 4px;
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
            }}
        """)
        
        layout_progresso = QHBoxLayout(progresso_frame)
        layout_progresso.setContentsMargins(10, 4, 10, 4)
        layout_progresso.setSpacing(10)
        
        # Label para progresso
        lbl_progresso = QLabel("Progresso:")
        lbl_progresso.setStyleSheet(f"""
            color: {TEMA_ATUAL['COR_TEXTO']};
            font-weight: bold;
            font-size: 13px;
            margin-right: 5px;
        """)
        layout_progresso.addWidget(lbl_progresso)
        
        # Barra de progresso - criar apenas se não existir
        if not hasattr(self, 'progresso') or self.progresso is None:
            self.progresso = QProgressBar()
            self.progresso.setRange(0, 100)
            self.progresso.setValue(0)
            self.progresso.setTextVisible(True)
            self.progresso.setFormat("%p%")
            self.progresso.setStyleSheet(f"""
                QProgressBar {{
                    background-color: {TEMA_ATUAL['COR_FUNDO']};
                    color: {TEMA_ATUAL['COR_TEXTO']};
                    border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                    border-radius: 5px;
                    text-align: center;
                    font-weight: bold;
                    height: 22px;
                    min-height: 22px;
                }}
                QProgressBar::chunk {{
                    background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                    border-radius: 4px;
                }}
            """)
        layout_progresso.addWidget(self.progresso, 1)
        
        layout.addWidget(progresso_frame)
        
    def selecionar_arquivo(self):
        options = QFileDialog.Options()
        arquivo, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Arquivo CNAB", "", 
            "Arquivos de Texto (*.txt *.TXT);;Todos os Arquivos (*)", 
            options=options
        )
        
        if arquivo:
            self.arquivo_atual = arquivo
            self.lbl_arquivo.setText(f"Arquivo: {os.path.basename(arquivo)}")
            self.btn_processar.setEnabled(True)
            # Resetar a tabela
            self.tabela.setRowCount(0)
            self.tabela.setColumnCount(0)
            self.btn_exportar_csv.setEnabled(False)
            self.btn_exportar_excel.setEnabled(False)
            self.btn_gerar_cnab.setEnabled(False)
            self.lbl_tabela.setText("Arquivo selecionado. Clique em 'Processar Arquivo' para continuar.")
            self.status_bar.showMessage(f"Arquivo selecionado: {os.path.basename(arquivo)}")
            
    def processar_arquivo(self):
        if not self.arquivo_atual or not os.path.exists(self.arquivo_atual):
            QMessageBox.warning(self, "Arquivo Inválido", "Por favor, selecione um arquivo válido primeiro.")
            return
        
        try:
            self.status_bar.showMessage("Processando arquivo...")
            self.progresso.setValue(10)
        
            # Processar o arquivo CNAB
            processador = CNABBradesco(self.arquivo_atual)
            self.processador = processador  # Atribuir à propriedade da classe
            if processador.ler_arquivo():
                self.progresso.setValue(50)
                
                # Converter para DataFrame para a tabela
                self.df = pd.DataFrame(processador.detalhes)
                
                # Preencher tabela
                self.preencher_tabela()
                
                # Preencher resumo com os dados
                self.preencher_resumo(processador)
                
                # Ativar os botões de exportação
                self.btn_exportar_csv.setEnabled(True)
                self.btn_exportar_excel.setEnabled(True)
                self.btn_gerar_cnab.setEnabled(True)
                
                # Habilitar outros botões de ação na aba de detalhes
                self.btn_exportar_csv.setEnabled(True)
                self.btn_exportar_excel.setEnabled(True)
                self.btn_gerar_cnab.setEnabled(True)
                
                self.progresso.setValue(100)
                self.status_bar.showMessage(f"Arquivo processado com sucesso. {len(self.df)} registros encontrados.")
            else:
                self.progresso.setValue(0)
                self.status_bar.showMessage("Erro ao processar o arquivo.")
                QMessageBox.critical(self, "Erro", "Não foi possível processar o arquivo CNAB.")
        except Exception as e:
            self.progresso.setValue(0)
            self.status_bar.showMessage(f"Erro: {str(e)}")
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao processar o arquivo:\n{str(e)}")
            
    def preencher_resumo(self, processador):
        """Preenche a aba de resumo com os dados do arquivo processado"""
        try:
            # Dados de cabeçalho
            if processador.header:
                # Data de geração
                data_str = processador.header.get('data_geracao', '')
                if data_str:
                    try:
                        data = f"{data_str[0:2]}/{data_str[2:4]}/{data_str[4:8]}"
                        self.valor_data.setText(data)
                    except:
                        self.valor_data.setText(data_str)
                else:
                    self.valor_data.setText("-")
                
                # Adicionar informação do cedente/empresa
                if 'nome_empresa' in processador.header:
                    # Criar labels dinâmicos para empresa
                    info_grid = self.info_arquivo.layout().itemAt(0).layout()
                    
                    # Nome da empresa
                    lbl_empresa = QLabel("Empresa:")
                    lbl_empresa.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold;")
                    valor_empresa = QLabel(processador.header.get('nome_empresa', '-'))
                    valor_empresa.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']};")
                    info_grid.addWidget(lbl_empresa, 2, 0)
                    info_grid.addWidget(valor_empresa, 2, 1)
            
            # Quantidade de títulos
            qtd_titulos = len(processador.detalhes)
            self.valor_registros.setText(str(qtd_titulos))
            
            # Cálculos financeiros
            valor_total = sum(float(detalhe.get('valor_titulo', 0)) for detalhe in processador.detalhes)
            valor_juros = sum(float(detalhe.get('valor_juros', 0)) for detalhe in processador.detalhes)
            valor_multa = sum(float(detalhe.get('valor_multa', 0)) for detalhe in processador.detalhes)
            valor_desconto = sum(float(detalhe.get('valor_desconto', 0)) for detalhe in processador.detalhes)
            valor_pago = sum(float(detalhe.get('valor_pago', 0)) for detalhe in processador.detalhes)
            valor_principal = valor_total - valor_juros - valor_multa
            
            # Atualizar labels com formatação monetária
            self.valor_total.setText(self.formatar_moeda(valor_total))
            self.valor_juros.setText(self.formatar_moeda(valor_juros))
            self.valor_multa.setText(self.formatar_moeda(valor_multa))
            self.valor_principal.setText(self.formatar_moeda(valor_principal))
            
            # Adicionar mais informações financeiras no layout existente
            financeiro_grid = self.info_financeira.layout().itemAt(0).layout()
            
            # Valor de descontos
            lbl_desconto = QLabel("Total de Descontos:")
            lbl_desconto.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold;")
            valor_desconto_lbl = QLabel(self.formatar_moeda(valor_desconto))
            valor_desconto_lbl.setStyleSheet(f"color: #28A745; font-weight: bold;")  # Verde para descontos
            financeiro_grid.addWidget(lbl_desconto, 4, 0)
            financeiro_grid.addWidget(valor_desconto_lbl, 4, 1)
            
            # Valor efetivamente pago
            lbl_efetivo = QLabel("Valor Efetivamente Pago:")
            lbl_efetivo.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold;")
            valor_efetivo = QLabel(self.formatar_moeda(valor_pago))
            valor_efetivo.setStyleSheet(f"color: {TEMA_ATUAL['COR_PRIMARIA']}; font-weight: bold;")
            financeiro_grid.addWidget(lbl_efetivo, 5, 0)
            financeiro_grid.addWidget(valor_efetivo, 5, 1)
            
            # Criar grupo para estatísticas de pagamento
            if not hasattr(self, 'info_estatisticas'):
                self.info_estatisticas = QGroupBox("Estatísticas de Pagamento")
                self.info_estatisticas.setStyleSheet(f"""
                    QGroupBox {{
                        font-size: 13px;
                        font-weight: bold;
                        border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                        border-radius: 6px;
                        margin-top: 12px;
                        background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                        color: {TEMA_ATUAL['COR_TEXTO']};
                        padding: 5px;
                    }}
                    QGroupBox::title {{
                        subcontrol-origin: margin;
                        left: 15px;
                        padding: 0 5px 0 5px;
                        color: {TEMA_ATUAL['COR_PRIMARIA']};
                    }}
                """)
                
                layout_estatisticas = QVBoxLayout(self.info_estatisticas)
                layout_estatisticas.setContentsMargins(15, 20, 15, 15)
                layout_estatisticas.setSpacing(12)
                
                # Grid para estatísticas
                estatisticas_grid = QGridLayout()
                estatisticas_grid.setColumnStretch(0, 0)  # Coluna de labels
                estatisticas_grid.setColumnStretch(1, 1)  # Coluna de valores
                estatisticas_grid.setSpacing(8)
                
                layout_estatisticas.addLayout(estatisticas_grid)
                
                # Adicionar ao layout principal
                self.info_arquivo.layout().parentWidget().layout().addWidget(self.info_estatisticas)
            
            # Obter o grid de estatísticas
            estatisticas_grid = self.info_estatisticas.layout().itemAt(0).layout()
            estatisticas_grid.setColumnStretch(0, 0)
            estatisticas_grid.setColumnStretch(1, 1)
            
            # Análise de ocorrências
            ocorrencias = {}
            for detalhe in processador.detalhes:
                cod = detalhe.get('cod_ocorrencia', '00')
                ocorrencias[cod] = ocorrencias.get(cod, 0) + 1
            
            # Mapeamento de códigos de ocorrência para descrições
            mapa_ocorrencias = {
                '02': 'Confirmação de Entrada',
                '03': 'Comando Recusado',
                '06': 'Liquidação Normal',
                '07': 'Liquidação por Conta',
                '08': 'Liquidação por Saldo',
                '09': 'Baixa Automática',
                '10': 'Baixa por Instrução',
                '11': 'Títulos em Ser',
                '12': 'Abatimento Concedido',
                '13': 'Abatimento Cancelado',
                '14': 'Prorrogação de Vencimento',
                '15': 'Liquidação em Cartório',
                '16': 'Alteração de Dados',
                '17': 'Liquidação após Baixa',
                '18': 'Acerto de Depositária',
                '19': 'Instrução Recusada',
                '20': 'Alteração de Dados do Remetente',
                '21': 'Alteração do Controle do Participante',
                '22': 'Alteração de Seu Número',
                '23': 'Confirmação de Instrução',
                '24': 'Débito em Conta',
                '25': 'Instrução Cancelada',
                '26': 'Tarifas Diversas',
                '27': 'Reembolso Despesas',
                '28': 'Alteração Juros de Mora',
                '29': 'Sustar Protesto',
                '30': 'Baixa Ou Liquidação',
                '31': 'Título Não Existe',
                '32': 'Título Já Baixado',
                '33': 'Título Já Liquidado',
                '34': 'Liquidação Parcial',
                '35': 'Confirmação de Instrução Automática'
            }
            
            # Limpar qualquer estatística anterior
            for i in reversed(range(estatisticas_grid.count())): 
                item = estatisticas_grid.itemAt(i)
                if item:
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
                        widget.deleteLater()
            
            # Calcular estatísticas
            titulos_liquidados = sum(ocorrencias.get(cod, 0) for cod in ['06', '07', '08', '15', '17'])
            titulos_baixados = sum(ocorrencias.get(cod, 0) for cod in ['09', '10'])
            titulos_pendentes = sum(ocorrencias.get(cod, 0) for cod in ['11'])
            
            # Exibir estatísticas principais
            lbl_liquidados = QLabel("Títulos Liquidados:")
            lbl_liquidados.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold;")
            valor_liquidados = QLabel(f"{titulos_liquidados} ({(titulos_liquidados/qtd_titulos*100 if qtd_titulos else 0):.2f}%)")
            valor_liquidados.setStyleSheet(f"color: #28A745; font-weight: bold;")
            estatisticas_grid.addWidget(lbl_liquidados, 0, 0)
            estatisticas_grid.addWidget(valor_liquidados, 0, 1)
            
            lbl_baixados = QLabel("Títulos Baixados:")
            lbl_baixados.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold;")
            valor_baixados = QLabel(f"{titulos_baixados} ({(titulos_baixados/qtd_titulos*100 if qtd_titulos else 0):.2f}%)")
            valor_baixados.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold;")
            estatisticas_grid.addWidget(lbl_baixados, 1, 0)
            estatisticas_grid.addWidget(valor_baixados, 1, 1)
            
            lbl_pendentes = QLabel("Títulos Pendentes:")
            lbl_pendentes.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold;")
            valor_pendentes = QLabel(f"{titulos_pendentes} ({(titulos_pendentes/qtd_titulos*100 if qtd_titulos else 0):.2f}%)")
            valor_pendentes.setStyleSheet(f"color: {TEMA_ATUAL['COR_DESTAQUE']}; font-weight: bold;")
            estatisticas_grid.addWidget(lbl_pendentes, 2, 0)
            estatisticas_grid.addWidget(valor_pendentes, 2, 1)
            
            # Separador
            separador = QFrame()
            separador.setFrameShape(QFrame.HLine)
            separador.setFrameShadow(QFrame.Sunken)
            separador.setStyleSheet(f"""
                background-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                max-height: 1px;
                margin-top: 10px;
                margin-bottom: 10px;
            """)
            estatisticas_grid.addWidget(separador, 3, 0, 1, 2)
            
            # Adicionar detalhes de ocorrências mais relevantes
            row = 4
            for cod in sorted(ocorrencias.keys()):
                if ocorrencias[cod] > 0:
                    desc = mapa_ocorrencias.get(cod, f"Ocorrência {cod}")
                    lbl_ocorrencia = QLabel(f"{desc}:")
                    lbl_ocorrencia.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold;")
                    valor_ocorrencia = QLabel(f"{ocorrencias[cod]} ({(ocorrencias[cod]/qtd_titulos*100 if qtd_titulos else 0):.2f}%)")
                    
                    # Colorir de acordo com o tipo de ocorrência
                    if cod in ['06', '07', '08', '15', '17']:  # Liquidações
                        valor_ocorrencia.setStyleSheet("color: #28A745;")
                    elif cod in ['09', '10']:  # Baixas
                        valor_ocorrencia.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']};")
                    elif cod in ['03', '19', '25']:  # Recusas
                        valor_ocorrencia.setStyleSheet(f"color: {TEMA_ATUAL['COR_DESTAQUE']};")
                    else:
                        valor_ocorrencia.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']};")
                        
                    estatisticas_grid.addWidget(lbl_ocorrencia, row, 0)
                    estatisticas_grid.addWidget(valor_ocorrencia, row, 1)
                    row += 1
            
        except Exception as e:
            print(f"Erro ao preencher resumo: {str(e)}")
    
    def preencher_tabela(self):
        if self.df is None or self.df.empty:
            self.lbl_tabela.setText("Nenhum dado para exibir")
            return
            
        try:
            # Colunas a exibir na tabela (ordem e seleção)
            colunas_exibir = [
                'nosso_numero', 'seu_numero', 'data_ocorrencia', 'data_vencimento',
                'valor_titulo', 'valor_principal', 'valor_juros_multa', 'data_credito'
            ]
            
            # Mapeamento para nomes amigáveis
            nomes_colunas = {
                'nosso_numero': 'Nosso Número',
                'seu_numero': 'Seu Número',
                'data_ocorrencia': 'Data Ocorrência',
                'data_vencimento': 'Data Vencimento',
                'valor_titulo': 'Valor Título',
                'valor_principal': 'Valor Principal',
                'valor_juros_multa': 'Juros Mora Multa',
                'data_credito': 'Data Crédito'
            }
            
            # Filtrar apenas as colunas que existem no DataFrame
            colunas_existentes = [col for col in colunas_exibir if col in self.df.columns]
            
            # Configurar a tabela
            self.tabela.setRowCount(len(self.df))
            self.tabela.setColumnCount(len(colunas_existentes))
            
            # Configurar cabeçalhos
            headers = [nomes_colunas[col] for col in colunas_existentes]
            self.tabela.setHorizontalHeaderLabels(headers)
            
            # Preencher dados
            for i, (_, row) in enumerate(self.df.iterrows()):
                for j, col in enumerate(colunas_existentes):
                    valor = row[col]
                    
                    # Formatação específica para cada tipo de coluna
                    if col in ['data_ocorrencia', 'data_vencimento', 'data_credito']:
                        try:
                            # Formatação de data
                            if valor and len(str(valor)) >= 6:
                                data_str = str(valor)
                                if len(data_str) == 6:  # DDMMAA
                                    data_formatada = f"{data_str[0:2]}/{data_str[2:4]}/20{data_str[4:6]}"
                                elif len(data_str) == 8:  # DDMMAAAA
                                    data_formatada = f"{data_str[0:2]}/{data_str[2:4]}/{data_str[4:8]}"
                                else:
                                    data_formatada = str(valor)
                                item = QTableWidgetItem(data_formatada)
                            else:
                                item = QTableWidgetItem(str(valor) if valor else "")
                        except (ValueError, TypeError, IndexError):
                            item = QTableWidgetItem(str(valor) if valor else "")
                        item.setTextAlignment(Qt.AlignCenter)
                    
                    elif col in ['valor_titulo', 'valor_principal', 'valor_juros_multa']:
                        # Formatação de valores monetários
                        try:
                            valor_float = float(valor) if valor else 0.0
                            valor_formatado = f"R$ {valor_float:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                            item = QTableWidgetItem(valor_formatado)
                        except (ValueError, TypeError):
                            item = QTableWidgetItem(str(valor) if valor else "R$ 0,00")
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    
                    else:
                        # Outros campos
                        item = QTableWidgetItem(str(valor) if valor else "")
                        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    
                    self.tabela.setItem(i, j, item)
            
            # Ajustar largura das colunas
            self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            
            # Mensagem informativa
            self.lbl_tabela.setText(f"Exibindo {len(self.df)} registros")
            
        except Exception as e:
            self.lbl_tabela.setText(f"Erro ao preencher tabela: {str(e)}")
            print(f"Erro ao preencher tabela: {str(e)}")
        
    def exportar_csv(self):
        if self.df is None or self.arquivo_atual is None:
            return
            
        nome_arquivo = os.path.basename(self.arquivo_atual)
        nome_base = os.path.splitext(nome_arquivo)[0]
        
        options = QFileDialog.Options()
        caminho_csv, _ = QFileDialog.getSaveFileName(
            self, "Salvar Arquivo CSV", f"{nome_base}_processado.csv",
            "Arquivos CSV (*.csv)", options=options
        )
        
        if caminho_csv:
            try:
                # Para o CSV, usamos os valores originais (não formatados)
                df_original = self.df.copy()
                if 'linha_original' in df_original.columns:
                    df_original = df_original.drop('linha_original', axis=1)
                
                df_original.to_csv(caminho_csv, index=False, sep=';')
                self.status_bar.showMessage(f"Dados exportados para {os.path.basename(caminho_csv)}")
                QMessageBox.information(self, "Exportação Concluída", 
                                        f"Os dados foram exportados com sucesso para:\n{caminho_csv}")
            except Exception as e:
                QMessageBox.critical(self, "Erro na Exportação", 
                                    f"Ocorreu um erro ao exportar os dados:\n{str(e)}")
    
    def exportar_excel(self):
        """Exporta os dados para um arquivo Excel"""
        if self.df is None or self.arquivo_atual is None or not hasattr(self, 'processador'):
            return
            
        nome_arquivo = os.path.basename(self.arquivo_atual)
        nome_base = os.path.splitext(nome_arquivo)[0]
        
        options = QFileDialog.Options()
        caminho_excel, _ = QFileDialog.getSaveFileName(
            self, "Salvar Arquivo Excel", f"{nome_base}_processado.xlsx",
            "Arquivos Excel (*.xlsx)", options=options
        )
        
        if caminho_excel:
            self.status_bar.showMessage("Exportando para Excel...")
            self.progresso.setValue(10)
            
            try:
                # Usar o método do processador para exportar para Excel
                sucesso, mensagem = self.processador.exportar_para_excel(caminho_excel)
                
                self.progresso.setValue(100)
                if sucesso:
                    self.status_bar.showMessage(f"Dados exportados para Excel: {os.path.basename(caminho_excel)}")
                    QMessageBox.information(self, "Exportação Excel Concluída", 
                                          f"Os dados foram exportados com sucesso para:\n{caminho_excel}")
                else:
                    self.status_bar.showMessage("Falha na exportação para Excel")
                    QMessageBox.critical(self, "Erro na Exportação", mensagem)
            except Exception as e:
                self.progresso.setValue(0)
                self.status_bar.showMessage(f"Erro: {str(e)}")
                QMessageBox.critical(self, "Erro na Exportação", 
                                    f"Ocorreu um erro ao exportar os dados para Excel:\n{str(e)}")
    
    def gerar_cnab_retorno(self):
        """Gera um arquivo CNAB de retorno sem juros/multa"""
        if not hasattr(self, 'processador') or self.arquivo_atual is None:
            return
            
        nome_arquivo = os.path.basename(self.arquivo_atual)
        nome_base = os.path.splitext(nome_arquivo)[0]
        
        options = QFileDialog.Options()
        caminho_cnab, _ = QFileDialog.getSaveFileName(
            self, "Salvar Arquivo CNAB de Retorno", f"{nome_base}_retorno.TXT",
            "Arquivos CNAB (*.TXT);;Todos os Arquivos (*)", options=options
        )
        
        if caminho_cnab:
            self.status_bar.showMessage("Gerando arquivo CNAB de retorno...")
            self.progresso.setValue(30)
            
            try:
                # Usar o método do processador para gerar o arquivo CNAB
                sucesso, mensagem = self.processador.gerar_cnab_retorno(caminho_cnab)
                
                self.progresso.setValue(100)
                if sucesso:
                    self.status_bar.showMessage(f"Arquivo CNAB de retorno gerado: {os.path.basename(caminho_cnab)}")
                    QMessageBox.information(self, "CNAB de Retorno Gerado", 
                                          f"O arquivo CNAB de retorno foi gerado com sucesso!\n\nCaminho: {caminho_cnab}\n\nTodos os valores de juros/multa foram zerados.")
                else:
                    self.status_bar.showMessage("Falha na geração do arquivo CNAB")
                    QMessageBox.critical(self, "Erro na Geração", mensagem)
            except Exception as e:
                self.progresso.setValue(0)
                self.status_bar.showMessage(f"Erro: {str(e)}")
                QMessageBox.critical(self, "Erro na Geração do CNAB", 
                                    f"Ocorreu um erro ao gerar o arquivo CNAB de retorno:\n{str(e)}")
    
    def excel_para_cnab(self):
        """Converte arquivo Excel para CNAB"""
        if not hasattr(self, 'processador') or not self.processador or not hasattr(self.processador, 'detalhes') or not self.processador.detalhes:
            QMessageBox.warning(self, "Aviso", "Primeiro carregue um arquivo CNAB.")
            return
        
        # Selecionar arquivo Excel
        arquivo_excel, _ = QFileDialog.getOpenFileName(
            self, 
            "Selecionar arquivo Excel", 
            "", 
            "Arquivos Excel (*.xlsx *.xls)"
        )
        
        if not arquivo_excel:
            return
        
        # Selecionar onde salvar o CNAB
        arquivo_cnab, _ = QFileDialog.getSaveFileName(
            self, 
            "Salvar arquivo CNAB", 
            "novo_arquivo.TXT", 
            "Arquivos CNAB (*.TXT)"
        )
        
        if not arquivo_cnab:
            return
        
        # Perguntar se quer usar arquivo de referência
        resposta = QMessageBox.question(
            self, 
            "Arquivo de Referência",
            "Deseja usar um arquivo CNAB de referência para header/trailer?\n\n"
            "Se não, será gerado um header/trailer padrão.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        arquivo_referencia = None
        if resposta == QMessageBox.Yes:
            arquivo_referencia, _ = QFileDialog.getOpenFileName(
                self, 
                "Selecionar arquivo CNAB de referência", 
                "", 
                "Arquivos CNAB (*.TXT)"
            )
        
        try:
            sucesso, mensagem = self.processador.excel_para_cnab(
                arquivo_excel, 
                arquivo_cnab, 
                arquivo_referencia
            )
            
            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
            else:
                QMessageBox.critical(self, "Erro", mensagem)
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao converter: {str(e)}")

    def editor_interativo(self):
        """Abre o editor interativo de CNAB"""
        if not hasattr(self, 'processador') or not self.processador or not hasattr(self.processador, 'detalhes') or not self.processador.detalhes:
            QMessageBox.warning(self, "Aviso", 
                "Primeiro carregue um arquivo CNAB para poder editá-lo.")
            return
        
        # Mostrar aviso sobre funcionalidade
        resposta = QMessageBox.question(
            self, 
            "Editor Interativo",
            "🔧 EDITOR INTERATIVO DE CNAB\n\n"
            "Esta funcionalidade permite:\n"
            "• Editar registros individuais\n"
            "• Alterar valores em lote\n"
            "• Modificar datas em massa\n"
            "• Visualizar e buscar registros\n"
            "• Salvar alterações em novo arquivo\n\n"
            "⚠️ O editor será aberto no terminal/console.\n"
            "Verifique a janela do terminal após clicar 'Yes'.\n\n"
            "Deseja continuar?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if resposta != QMessageBox.Yes:
            return
        
        try:
            # Executar editor interativo em thread separada para não travar a GUI
            import threading
            
            def executar_editor():
                resultado = self.processador.editor_interativo()
                if resultado:
                    # Se salvou alterações, atualizar a visualização
                    self.atualizar_visualizacao()
            
            # Criar e iniciar thread
            thread_editor = threading.Thread(target=executar_editor)
            thread_editor.daemon = True
            thread_editor.start()
            
            # Mostrar informação sobre onde encontrar o editor
            QMessageBox.information(
                self, 
                "Editor Iniciado",
                "🔧 Editor interativo iniciado!\n\n"
                "📍 Verifique a janela do terminal/console\n"
                "   para interagir com o editor.\n\n"
                "💡 Se não conseguir ver o terminal:\n"
                "   • Windows: Procure por uma janela preta\n"
                "   • Use Alt+Tab para alternar entre janelas\n\n"
                "✅ A interface gráfica permanecerá responsiva."
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", 
                f"Erro ao iniciar editor interativo: {str(e)}")

    def editor_grafico(self):
        """Abre o editor gráfico para NOSSO_NUMERO, CODIGO_EMPRESA e SEU_NUMERO"""
        if not hasattr(self, 'processador') or not self.processador or not hasattr(self.processador, 'detalhes') or not self.processador.detalhes:
            QMessageBox.warning(self, "Aviso", 
                "Primeiro carregue um arquivo CNAB para poder editá-lo.")
            return
        
        try:
            # Criar e abrir o dialog do editor gráfico
            dialog = EditorGraficoDialog(self.processador, self)
            resultado = dialog.exec_()
            
            # Se o usuário salvou alterações, atualizar a visualização
            if resultado == QDialog.Accepted:
                self.atualizar_visualizacao()
                self.status_bar.showMessage("Alterações aplicadas com sucesso!")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", 
                f"Erro ao abrir editor gráfico: {str(e)}")

    def atualizar_visualizacao(self):
        """Atualiza a visualização após alterações no editor"""
        try:
            # Recarregar dados na tabela
            if hasattr(self, 'processador') and self.processador and hasattr(self.processador, 'detalhes') and self.processador.detalhes:
                # Atualizar DataFrame
                self.df = pd.DataFrame(self.processador.detalhes)
                self.preencher_tabela()
                
                # Mostrar mensagem de atualização
                alterados = len([d for d in self.processador.detalhes if d.get('_alterado', False)])
                if alterados > 0:
                    QMessageBox.information(
                        self, 
                        "Dados Atualizados",
                        f"✅ Visualização atualizada!\n\n"
                        f"📊 {alterados} registro(s) foram alterados\n"
                        f"📄 Total de registros: {len(self.processador.detalhes)}"
                    )
        except Exception as e:
            print(f"Erro ao atualizar visualização: {e}")

    def _criar_aba_detalhes(self, layout):
        # Container principal da tabela
        tabela_container = QFrame()
        tabela_container.setStyleSheet(f"""
            QFrame {{
                background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                border-radius: 8px;
                padding: 8px;
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
            }}
        """)
        layout_tabela = QVBoxLayout(tabela_container)
        layout_tabela.setContentsMargins(12, 12, 12, 12)
        layout_tabela.setSpacing(12)
        
        # Cabeçalho da tabela com informações
        header_container = QHBoxLayout()
        header_container.setSpacing(10)
        
        # Ícone para a tabela
        icon_tabela = QLabel("📋")
        icon_tabela.setStyleSheet(f"""
            font-size: 20px;
            color: {TEMA_ATUAL['COR_PRIMARIA']};
        """)
        header_container.addWidget(icon_tabela)
        
        # Label para a tabela
        self.lbl_tabela = QLabel("Nenhum dado para exibir")
        self.lbl_tabela.setStyleSheet(f"""
            color: {TEMA_ATUAL['COR_TEXTO']};
            font-size: 14px;
            font-weight: bold;
            font-family: 'Segoe UI';
        """)
        header_container.addWidget(self.lbl_tabela, 1)
        
        layout_tabela.addLayout(header_container)
        
        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setFrameShadow(QFrame.Sunken)
        separador.setStyleSheet(f"""
            background-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
            max-height: 1px;
            margin-top: 8px;
            margin-bottom: 8px;
        """)
        layout_tabela.addWidget(separador)
        
        # Tabela para exibição dos dados - criar apenas se não existir
        if not hasattr(self, 'tabela') or self.tabela is None:
            self.tabela = QTableWidget()
            self.tabela.setStyleSheet(f"""
                QTableWidget {{
                    background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                    color: {TEMA_ATUAL['COR_TEXTO']};
                    gridline-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                    border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                    border-radius: 8px;
                    padding: 2px;
                }}
                QTableWidget::item {{
                    padding: 8px;
                    border-bottom: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                }}
                QTableWidget::item:selected {{
                    background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                    color: white;
                }}
                QHeaderView::section {{
                    background-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                    color: {TEMA_ATUAL['COR_TEXTO']};
                    padding: 10px;
                    border: none;
                    font-weight: bold;
                    text-align: center;
                }}
                QTableWidget QTableCornerButton::section {{
                    background-color: {TEMA_ATUAL['COR_TABELA_HEADER']};
                    border: none;
                }}
            """)
            self.tabela.setAlternatingRowColors(True)
            self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
            self.tabela.setSelectionMode(QTableWidget.SingleSelection)
            self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
            self.tabela.horizontalHeader().setStretchLastSection(True)
            self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
            self.tabela.verticalHeader().setVisible(False)
        layout_tabela.addWidget(self.tabela, 1)
        
        layout.addWidget(tabela_container, 1)
        
    def _criar_aba_resumo(self, layout):
        # Container principal
        container_principal = QScrollArea()
        container_principal.setWidgetResizable(True)
        container_principal.setStyleSheet(f"""
            QScrollArea {{
                background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                border-radius: 8px;
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                padding: 4px;
            }}
            QScrollBar:vertical {{
                border: none;
                background: {TEMA_ATUAL['COR_TABELA_HEADER']};
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {TEMA_ATUAL['COR_PRIMARIA']};
                border-radius: 5px;
                min-height: 30px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        scroll_content = QWidget()
        layout_scroll = QVBoxLayout(scroll_content)
        layout_scroll.setContentsMargins(16, 16, 16, 16)
        layout_scroll.setSpacing(16)
        
        # Grupo para informações do arquivo
        self.info_arquivo = QGroupBox("Informações do Arquivo")
        self.info_arquivo.setStyleSheet(f"""
            QGroupBox {{
                font-size: 14px;
                font-weight: bold;
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                border-radius: 8px;
                margin-top: 16px;
                background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                color: {TEMA_ATUAL['COR_TEXTO']};
                padding: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 5px 0 5px;
                color: {TEMA_ATUAL['COR_PRIMARIA']};
            }}
        """)
        
        layout_info = QVBoxLayout(self.info_arquivo)
        layout_info.setContentsMargins(16, 24, 16, 16)
        layout_info.setSpacing(12)
        
        # Campos de informação com layout em grid para alinhamento
        info_grid = QGridLayout()
        info_grid.setColumnStretch(0, 0)  # Coluna de labels
        info_grid.setColumnStretch(1, 1)  # Coluna de valores
        info_grid.setSpacing(10)
        
        # Data de geração
        lbl_data = QLabel("Data de Geração:")
        lbl_data.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold; font-size: 13px;")
        self.valor_data = QLabel("-")
        self.valor_data.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-size: 13px;")
        info_grid.addWidget(lbl_data, 0, 0)
        info_grid.addWidget(self.valor_data, 0, 1)
        
        # Número de registros
        lbl_registros = QLabel("Número de Registros:")
        lbl_registros.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold; font-size: 13px;")
        self.valor_registros = QLabel("-")
        self.valor_registros.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-size: 13px;")
        info_grid.addWidget(lbl_registros, 1, 0)
        info_grid.addWidget(self.valor_registros, 1, 1)
        
        layout_info.addLayout(info_grid)
        
        layout_scroll.addWidget(self.info_arquivo)
        
        # Grupo para totais financeiros
        self.info_financeira = QGroupBox("Informações Financeiras")
        self.info_financeira.setStyleSheet(f"""
            QGroupBox {{
                font-size: 14px;
                font-weight: bold;
                border: 1px solid {TEMA_ATUAL['COR_TABELA_HEADER']};
                border-radius: 8px;
                margin-top: 16px;
                background-color: {TEMA_ATUAL['COR_SECUNDARIA']};
                color: {TEMA_ATUAL['COR_TEXTO']};
                padding: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 5px 0 5px;
                color: {TEMA_ATUAL['COR_PRIMARIA']};
            }}
        """)
        
        layout_financeiro = QVBoxLayout(self.info_financeira)
        layout_financeiro.setContentsMargins(16, 24, 16, 16)
        layout_financeiro.setSpacing(12)
        
        # Grid para valores financeiros
        financeiro_grid = QGridLayout()
        financeiro_grid.setColumnStretch(0, 0)  # Coluna de labels
        financeiro_grid.setColumnStretch(1, 1)  # Coluna de valores
        financeiro_grid.setSpacing(10)
        
        # Valor total
        lbl_total = QLabel("Valor Total:")
        lbl_total.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold; font-size: 13px;")
        self.valor_total = QLabel("-")
        self.valor_total.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-size: 13px;")
        financeiro_grid.addWidget(lbl_total, 0, 0)
        financeiro_grid.addWidget(self.valor_total, 0, 1)
        
        # Valor juros
        lbl_juros = QLabel("Total de Juros:")
        lbl_juros.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold; font-size: 13px;")
        self.valor_juros = QLabel("-")
        self.valor_juros.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-size: 13px;")
        financeiro_grid.addWidget(lbl_juros, 1, 0)
        financeiro_grid.addWidget(self.valor_juros, 1, 1)
        
        # Valor multa
        lbl_multa = QLabel("Total de Multas:")
        lbl_multa.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold; font-size: 13px;")
        self.valor_multa = QLabel("-")
        self.valor_multa.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-size: 13px;")
        financeiro_grid.addWidget(lbl_multa, 2, 0)
        financeiro_grid.addWidget(self.valor_multa, 2, 1)
        
        # Valor principal
        lbl_principal = QLabel("Valor Principal:")
        lbl_principal.setStyleSheet(f"color: {TEMA_ATUAL['COR_TEXTO']}; font-weight: bold; font-size: 13px;")
        self.valor_principal = QLabel("-")
        self.valor_principal.setStyleSheet(f"color: {TEMA_ATUAL['COR_PRIMARIA']}; font-weight: bold; font-size: 13px;")
        financeiro_grid.addWidget(lbl_principal, 3, 0)
        financeiro_grid.addWidget(self.valor_principal, 3, 1)
        
        layout_financeiro.addLayout(financeiro_grid)
        
        layout_scroll.addWidget(self.info_financeira)
        
        # Adicionar espaço extra
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout_scroll.addWidget(spacer)
        
        container_principal.setWidget(scroll_content)
        layout.addWidget(container_principal, 1)

    def formatar_moeda(self, valor):
        """Formata um valor para o padrão monetário brasileiro"""
        return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')


def main():
    app = QApplication(sys.argv)
    
    # Configurar estilo global
    app.setStyle("Fusion")
    
    window = CNABBradescoGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 