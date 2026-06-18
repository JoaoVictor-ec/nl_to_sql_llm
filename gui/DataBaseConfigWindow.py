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

from sqlalchemy import  inspect

#classe reponsável pelas funcionalidades da janela de config do db
class DatabaseConfigDialog(QDialog):

    def __init__(self):
        super().__init__()

        #define o titulo da janela e o tamanho que ela terá
        self.setWindowTitle("Configuração do Banco")
        self.resize(450, 300)

        self.setup_ui()

    #função que faz a construção da janela.
    def setup_ui(self):

        layout = QVBoxLayout()#layout da base vertical

        # lista que mostra os tipos de banco possíveis
        self.db_type = QComboBox()
        self.db_type.addItems([
            "MySQL",
            "PostgreSQL"
        ])

        # seta o host para local host inicialmente, o usuário pode mudar se o dele não for
        self.host_input = QLineEdit()
        self.host_input.setText("localhost")

        # seta a porta para 3306 incialmente, o usuário pode mudar se necessário
        self.port_input = QLineEdit()
        self.port_input.setText("3306")

        #pega o nome do banco
        self.database_input = QLineEdit()

        # pega o user do banco (Ex: root)
        self.user_input = QLineEdit()

        # pega a senha do banco de dados
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(  # faz aparecer as bolinhas ao inves do texto
            QLineEdit.Password
        )

        # adiciona visualmente os campos a janela 
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

        button_layout = QHBoxLayout()#layout horizontal

        # cria os botões 
        self.test_button = QPushButton(
            "Testar Conexão"
        )

        self.save_button = QPushButton(
            "Salvar"
        )

        self.cancel_button = QPushButton(
            "Cancelar"
        )

        #organiza eles vizualmente
        button_layout.addWidget(
            self.test_button
        )

        button_layout.addStretch() # deixa um espaço entre eles

        button_layout.addWidget(
            self.save_button
        )

        button_layout.addWidget(
            self.cancel_button
        )

        layout.addLayout(button_layout) #adiciona ao layout principal

        self.setLayout(layout)#aplica os layouts na janela

        #chama as funções baseado no botão que foi apertado
        
        #cancela e fecha a janela
        self.cancel_button.clicked.connect(
            self.reject
        )

        #salva e fecha a janela
        self.save_button.clicked.connect(
            self.accept
        )

        #testa e abre outra janela
        self.test_button.clicked.connect(
            self.test_connection
        )

    #função que pega os valores dos campos de config e então cria uma conxeção com o banco de dados.
    def test_connection(self):

        #tenta pegar os valores dos campos e estabelecer uma conexão
        try:
            
            config = {
                "db_type": self.db_type.currentText(),
                "host": self.host_input.text(),
                "port": self.port_input.text(),
                "database": self.database_input.text(),
                "user": self.user_input.text(),
                "password": self.password_input.text()
            }

            # cria uma string de conexão e escolher o driver baseado no tipo de banco escolhido
            engine = DatabaseConnection.create_engine_from_config(
                config
            )

            #inspeciona o banco de dados e pega o nome das tabelas
            inspector = inspect(engine)
            tables = inspector.get_table_names()

            # mostra uma mensagem em outra janela que conectou e o nome da database
            message = (
                f"Conectado ao banco: "
                f"{config['database']}\n\n"
            )

            #se o inspetor achar tabelas, ele inclui na mensagem as que encontrou
            if tables:

                message += "Tabelas encontradas:\n"

                for table in tables:
                    message += f"• {table}\n"

            else:

                message += (
                    "Nenhuma tabela encontrada."
                )

            #mostra a mensagem em uma janelinha
            QMessageBox.information(
                self,
                "Sucesso",
                message
            )
        
        #caso tenha algo errado nas infos de conexão ou algo do tipo mostra uma janelinha de erro
        except Exception as e:

            QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    # função que retorna as configs do banco, é usada para conseguir elas na janela principal (MainWindow)
    def get_config(self):

        return {
            "db_type": self.db_type.currentText(),
            "host": self.host_input.text(),
            "port": self.port_input.text(),
            "database": self.database_input.text(),
            "user": self.user_input.text(),
            "password": self.password_input.text()
        }