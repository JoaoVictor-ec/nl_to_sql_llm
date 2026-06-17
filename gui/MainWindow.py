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
from DataBase.connection import DatabaseConnection
from DataBase.SchemaLoader import SchemaLoader
from DataBase.QueryExecutor import QueryExecutor

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

        # ==================================================
        # Dados fictícios para teste visual
        # ==================================================

        self.populate_test_data()

    def open_database_config(self):

        dialog = DatabaseConfigDialog()

        if dialog.exec():

            self.db_config = dialog.get_config()

            self.status_output.append(
                "Banco configurado com sucesso."
            )

    def populate_test_data(self):

        self.sql_output.setText(
            """
SELECT c.nome,
       COUNT(*) AS total
FROM CLIENTE c
GROUP BY c.nome;
            """.strip()
        )

        self.status_output.setText(
            "Sistema iniciado com sucesso."
        )

        data = [
            [1, "João", 15],
            [2, "Maria", 12],
            [3, "Carlos", 9]
        ]

        self.result_table.setRowCount(len(data))

        for row_idx, row in enumerate(data):

            for col_idx, value in enumerate(row):

                item = QTableWidgetItem(str(value))

                item.setTextAlignment(Qt.AlignCenter)

                self.result_table.setItem(
                    row_idx,
                    col_idx,
                    item
                )


    def generate_sql(self):

        if not self.db_config:

            self.status_output.append(
                "Configure o banco primeiro."
            )

            return

        try:

            question = (
                self.question_input.toPlainText()
            )

            engine = (
                DatabaseConnection
                .create_engine_from_config(
                    self.db_config
                )
            )

            schema = (
                SchemaLoader
                .load_schema(engine)
            )

            schema_text = (
                SchemaLoader
                .schema_to_text(schema)
            )

            sql = self.llm.generate_sql(
                schema_text,
                question
            )
            columns, rows = QueryExecutor.execute(
                engine,
                sql
            )

            self.sql_output.setText(sql)

            self.populate_results(
                columns,
                rows
            )

            self.status_output.append(
                "SQL gerado com sucesso."
            )

        except Exception as e:

            self.status_output.append(
                f"Erro: {e}"
            )
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