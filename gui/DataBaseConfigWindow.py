from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox
)

from DataBase.connection import DatabaseConnection

from sqlalchemy import text, inspect

class DatabaseConfigDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Configuração do Banco")
        self.resize(450, 300)

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        # Tipo do banco

        self.db_type = QComboBox()
        self.db_type.addItems([
            "MySQL",
            "PostgreSQL"
        ])

        # Host

        self.host_input = QLineEdit()
        self.host_input.setText("localhost")

        # Porta

        self.port_input = QLineEdit()
        self.port_input.setText("3306")

        # Banco

        self.database_input = QLineEdit()

        # Usuário

        self.user_input = QLineEdit()

        # Senha

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(
            QLineEdit.Password
        )

        layout.addWidget(QLabel("Tipo"))
        layout.addWidget(self.db_type)

        layout.addWidget(QLabel("Host"))
        layout.addWidget(self.host_input)

        layout.addWidget(QLabel("Porta"))
        layout.addWidget(self.port_input)

        layout.addWidget(QLabel("Banco"))
        layout.addWidget(self.database_input)

        layout.addWidget(QLabel("Usuário"))
        layout.addWidget(self.user_input)

        layout.addWidget(QLabel("Senha"))
        layout.addWidget(self.password_input)

        # Botões

        button_layout = QHBoxLayout()

        self.test_button = QPushButton(
            "Testar Conexão"
        )

        self.save_button = QPushButton(
            "Salvar"
        )

        self.cancel_button = QPushButton(
            "Cancelar"
        )

        button_layout.addWidget(
            self.test_button
        )

        button_layout.addStretch()

        button_layout.addWidget(
            self.save_button
        )

        button_layout.addWidget(
            self.cancel_button
        )

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.cancel_button.clicked.connect(
            self.reject
        )

        self.save_button.clicked.connect(
            self.accept
        )

        self.test_button.clicked.connect(
            self.test_connection
        )

    def test_connection(self):

        try:

            config = {
                "db_type": self.db_type.currentText(),
                "host": self.host_input.text(),
                "port": self.port_input.text(),
                "database": self.database_input.text(),
                "user": self.user_input.text(),
                "password": self.password_input.text()
            }

            engine = DatabaseConnection.create_engine_from_config(
                config
            )

            inspector = inspect(engine)

            tables = inspector.get_table_names()

            message = (
                f"Conectado ao banco: "
                f"{config['database']}\n\n"
            )

            if tables:

                message += "Tabelas encontradas:\n"

                for table in tables:
                    message += f"• {table}\n"

            else:

                message += (
                    "Nenhuma tabela encontrada."
                )

            QMessageBox.information(
                self,
                "Sucesso",
                message
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    def get_config(self):

        return {
            "db_type": self.db_type.currentText(),
            "host": self.host_input.text(),
            "port": self.port_input.text(),
            "database": self.database_input.text(),
            "user": self.user_input.text(),
            "password": self.password_input.text()
        }