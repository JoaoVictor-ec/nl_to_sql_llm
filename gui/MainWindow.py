from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QGroupBox,
    QComboBox
)
from gui.DataBaseConfigWindow import (
    DatabaseConfigDialog
)
from llm.OllamaClient import OllamaClient
from llm.SqlWorker import SQLWorker

from PySide6.QtCore import QThread

#classe da janela principal
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.db_config = None #atributo que irá armazenar as configs do banco de dados

        self.llm = OllamaClient() #cria uma instancia da classe OllamaClient

        #define tamanho e título da página
        self.setWindowTitle("NL to SQL")
        self.resize(1100, 750)

        self.setup_ui()

    #metodo responsável por criar a interface gráfica
    def setup_ui(self):

        #cria um widget para a janela principal, e um conteiner para as outras informações serem inseridas
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        #cria uma caixa escrito Configurações
        config_group = QGroupBox("Configurações")

        #define o layout de como organizar as caixas, aqui será horizontal
        config_layout = QHBoxLayout()

        #lista suspensa dos modelos que estarão disponíveis na caixa, não está implementado para ativamente carregar diferentes modelos
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "qwen3:14b"
        ])

        #cria a caixa de seleção do modelo
        config_layout.addWidget(QLabel("Modelo:"))

        #insere a lista suspensa dos modelos
        config_layout.addWidget(self.model_combo)

        #cria o botão de configurar o banco de dados
        self.database_button = QPushButton(
            "Configurar Banco"
        )

        #insere no layout o botão
        config_layout.addWidget(
            self.database_button
        )

        config_layout.addStretch()#espaço vazio para que os botões não se encostem

        config_group.setLayout(config_layout)#aplica o layout a janela principal

        #cria a seção Consulta em Linguagem Natural
        question_group = QGroupBox("Consulta em Linguagem Natural")
        question_layout = QVBoxLayout()#define o layout vetical

        #pega o input do teclado, onde a pessoa colocará a consulta em LN
        self.question_input = QTextEdit()

        #define um texto apagadinho de fundo como exemplo, exibe quando ta vazio
        self.question_input.setPlaceholderText(
            "Ex: Quais clientes realizaram mais pedidos?"
        )

        # inclui no layout principal
        question_layout.addWidget(self.question_input)

        question_group.setLayout(question_layout)

        #layout do botão de consulta
        button_layout = QHBoxLayout()

        self.query_button = QPushButton("Consultar")
        
        #centraliza o botão
        button_layout.addStretch()
        
        #adiciona ao layout principal
        button_layout.addWidget(self.query_button)
        button_layout.addStretch()

        #cria o layout da parte que vai mostrar o sql gerado pela llm
        sql_group = QGroupBox("SQL Gerado")
        sql_layout = QVBoxLayout()#define layout vertical

        # campo de exibição do sql gerado pela llm
        self.sql_output = QTextEdit()
        self.sql_output.setReadOnly(True)# garante que o usuário não poderá alterar o texto

        # adiciona ao layout principal
        sql_layout.addWidget(self.sql_output)
        sql_group.setLayout(sql_layout)

        #layout do log de mensagens, mostra qunado ele ainda ta gerando a query, quando acaba de gerar ela com sucesso, se conseguiu conexão com o banco, ...
        status_group = QGroupBox("Mensagens")

        status_layout = QVBoxLayout()#layout Vertical

        #define só saida, assim não da pro usuário escrever no log
        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)

        #define altura máxima, assim quando da um certo tamanho de log, o usuário tem que scrolar para baixo
        self.status_output.setMaximumHeight(120)

        #adiciona ao layout principal
        status_layout.addWidget(self.status_output)
        status_group.setLayout(status_layout)

        #layout dos resultados das buscas
        result_group = QGroupBox("Resultado da Consulta")

        result_layout = QVBoxLayout()#vertical

        #define o campo da tabela
        self.result_table = QTableWidget()

        #config inicial, para não começar vazio
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(
            ["ID", "Nome", "Total"]
        )

        # faz um ajuste automático, assim as colunas ocupam todo o espaço disponível
        self.result_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        
        #adiciona ao layout principal
        result_layout.addWidget(self.result_table)
        result_group.setLayout(result_layout)

        # Layout principal, junta as janelas criadas anteriormente em ordem
        main_layout.addWidget(config_group)
        main_layout.addWidget(question_group)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(sql_group)
        main_layout.addWidget(status_group)
        main_layout.addWidget(result_group)

        # faz a conexão dos botões, assim quando o usuário clicar ele chama a respectiva função
        self.database_button.clicked.connect(self.open_database_config)
        self.query_button.clicked.connect(self.generate_sql)

        # mensagem inicial
        self.status_output.setText(
            "Sistema iniciado."
        )

    #função que chama a janela de configuração do banco de dados
    def open_database_config(self):

        dialog = DatabaseConfigDialog()

        #bloqueia a janela principal até fechar a janela de config, caso o usuário clique em salvar, da true e entra no if, se clicar no cancelar da false
        if dialog.exec():

            # se o usuário clicar em salvar, ele pega a config do banco de dados para guardar e usar na janela principal
            self.db_config = dialog.get_config()

            #escreve uma mensagem de sucesso
            self.status_output.append(
                "Banco configurado com sucesso."
            )

    #função que mostra para o usuário que o modelo está gerando o sql e avisa quando está pronto, além de mostrar ele na janela principal, também pega a entrada dele
    def generate_sql(self):

        # verifica se existe uma config de banco de dados salva
        if not self.db_config:

            self.status_output.append(
                "Configure o banco primeiro."
            )

            return

        # pega a entrada do usuário em NL
        question = (
            self.question_input.toPlainText()
        )

        # mostra que a llm está pensando
        self.status_output.append(
            "Gerando SQL..."
        )

        # limpa o output anterior
        self.sql_output.clear()
        self.result_table.clearContents()

        self.query_button.setEnabled(False)#bloqueia o botão de consulta enquanto a llm pensa

        self.thread = QThread()#cria uma thread separada para não travar o python

        # cria uma instancia da classe SQLWorker
        self.worker = SQLWorker(
            self.llm, #modelo usado
            self.db_config, #conexão com o banco
            question #input do usuário
        )

        #faz o worker rodar fora da thread da janela principal, garantindo que nada irá travar
        self.worker.moveToThread(
            self.thread
        )

        # chama a função run do worker
        self.thread.started.connect(
            self.worker.run
        )

        # quando o processo termina mostra o sql, e preenche a tabela do que retornou do sql
        self.worker.finished.connect(
            self.on_sql_generated
        )

        # mostra erro caso ocorra, por query errada ou outros motivos
        self.worker.error.connect(
            self.on_sql_error
        )

        # encerra a thread
        self.worker.finished.connect(
            self.thread.quit
        )
        # deleta a instancia do worker
        self.worker.finished.connect(
            self.worker.deleteLater
        )
        # deleta o worker em caso de erro
        self.worker.error.connect(
            self.worker.deleteLater
        )

        # apaga a thread, para evitar vazar memória
        self.thread.finished.connect(
            self.thread.deleteLater
        )

        #encerra a thread em caso de erro
        self.worker.error.connect(
            self.thread.quit
        )

        self.thread.start() # inicia a thread, assim iniciando o fluxo real
    
    #recebe as colunas e linhas, e então preenche uma tabela
    def populate_results(self, columns, rows):

        # limpa a tabela antes
        self.result_table.clear()

        #conta o número de colunas
        self.result_table.setColumnCount(
            len(columns)
        )
        # preenche a o "cabeçalho" dela usando uma lista dos campos
        self.result_table.setHorizontalHeaderLabels(
            list(columns)
        )

        #conta o numero de linhas
        self.result_table.setRowCount(
            len(rows)
        )

        # percorre as linhas e colunas setando os valores em cada célula da tabela
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                
                # passa o valor que será inserido para string normalizando ele (necessário por vários motivos, o mais simples é blob por exemplo)
                item = QTableWidgetItem(
                    str(value)
                )
                # insere o valor na celula
                self.result_table.setItem(
                    row_idx,
                    col_idx,
                    item
                )

        self.result_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

    #callbacks
    #seta sql gerado, chama a função que preenche a tabela e seta ela tambem
    def on_sql_generated(self, result):

        self.sql_output.setText(
            result["sql"]
        )

        self.populate_results(
            result["columns"],
            result["rows"]
        )
        #mensagem avisando que o processo correu bem
        self.status_output.append(
            "Consulta executada com sucesso."
        )

        self.query_button.setEnabled(True)

    # caso tenha algum erro apenas mostra erro
    def on_sql_error(self, error):

        self.status_output.append(
            f"Erro: {error}"
        )

        self.query_button.setEnabled(True)