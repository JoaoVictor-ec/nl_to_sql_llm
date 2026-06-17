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


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.db_config = None

        self.llm = OllamaClient()

        self.setWindowTitle("NL to SQL")
        self.resize(1100, 750)

        self.setup_ui()

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # ==================================================
        # Configurações
        # ==================================================

        config_group = QGroupBox("Configurações")
        config_layout = QHBoxLayout()

        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "qwen3:14b"
        ])

        config_layout.addWidget(QLabel("Modelo:"))
        config_layout.addWidget(self.model_combo)

        self.database_button = QPushButton(
            "Configurar Banco"
        )

        config_layout.addWidget(
            self.database_button
        )

        config_layout.addStretch()

        config_group.setLayout(config_layout)

        # ==================================================
        # Pergunta
        # ==================================================

        question_group = QGroupBox("Consulta em Linguagem Natural")
        question_layout = QVBoxLayout()

        self.question_input = QTextEdit()
        self.question_input.setPlaceholderText(
            "Ex: Quais clientes realizaram mais pedidos?"
        )

        question_layout.addWidget(self.question_input)

        question_group.setLayout(question_layout)

        # ==================================================
        # Botão
        # ==================================================

        button_layout = QHBoxLayout()

        self.query_button = QPushButton("Consultar")

        button_layout.addStretch()
        button_layout.addWidget(self.query_button)
        button_layout.addStretch()

        # ==================================================
        # SQL Gerado
        # ==================================================

        sql_group = QGroupBox("SQL Gerado")

        sql_layout = QVBoxLayout()

        self.sql_output = QTextEdit()
        self.sql_output.setReadOnly(True)

        sql_layout.addWidget(self.sql_output)

        sql_group.setLayout(sql_layout)

        # ==================================================
        # Status
        # ==================================================

        status_group = QGroupBox("Mensagens")

        status_layout = QVBoxLayout()

        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)
        self.status_output.setMaximumHeight(120)

        status_layout.addWidget(self.status_output)

        status_group.setLayout(status_layout)

        # ==================================================
        # Resultado
        # ==================================================

        result_group = QGroupBox("Resultado da Consulta")

        result_layout = QVBoxLayout()

        self.result_table = QTableWidget()

        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(
            ["ID", "Nome", "Total"]
        )

        self.result_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        result_layout.addWidget(self.result_table)

        result_group.setLayout(result_layout)

        # ==================================================
        # Layout principal
        # ==================================================

        main_layout.addWidget(config_group)
        main_layout.addWidget(question_group)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(sql_group)
        main_layout.addWidget(status_group)
        main_layout.addWidget(result_group)

        self.database_button.clicked.connect(self.open_database_config)
        self.query_button.clicked.connect(self.generate_sql)

        self.status_output.setText(
            "Sistema iniciado."
        )


    def open_database_config(self):

        dialog = DatabaseConfigDialog()

        if dialog.exec():

            self.db_config = dialog.get_config()

            self.status_output.append(
                "Banco configurado com sucesso."
            )

    def generate_sql(self):

        if not self.db_config:

            self.status_output.append(
                "Configure o banco primeiro."
            )

            return

        question = (
            self.question_input.toPlainText()
        )

        self.status_output.append(
            "Gerando SQL..."
        )

        self.sql_output.clear()
        self.result_table.clearContents()

        self.query_button.setEnabled(False)

        self.thread = QThread()

        self.worker = SQLWorker(
            self.llm,
            self.db_config,
            question
        )

        self.worker.moveToThread(
            self.thread
        )

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.finished.connect(
            self.on_sql_generated
        )

        self.worker.error.connect(
            self.on_sql_error
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.finished.connect(
            self.worker.deleteLater
        )

        self.worker.error.connect(
            self.worker.deleteLater
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )
        self.worker.error.connect(
            self.thread.quit
        )

        self.thread.start()    
    
    def populate_results(self, columns, rows):

        self.result_table.clear()

        self.result_table.setColumnCount(
            len(columns)
        )

        self.result_table.setHorizontalHeaderLabels(
            list(columns)
        )

        self.result_table.setRowCount(
            len(rows)
        )

        for row_idx, row in enumerate(rows):

            for col_idx, value in enumerate(row):

                item = QTableWidgetItem(
                    str(value)
                )

                self.result_table.setItem(
                    row_idx,
                    col_idx,
                    item
                )

        self.result_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

    #callbacks

    def on_sql_generated(self, result):

        self.sql_output.setText(
            result["sql"]
        )

        self.populate_results(
            result["columns"],
            result["rows"]
        )

        self.status_output.append(
            "Consulta executada com sucesso."
        )

        self.query_button.setEnabled(True)
    
    def on_sql_error(self, error):

        self.status_output.append(
            f"Erro: {error}"
        )

        self.query_button.setEnabled(True)