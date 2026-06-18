from sqlalchemy import create_engine

# classe responsável por criar uma conexão com o banco de dados a partir de um dicionário de informações.
class DatabaseConnection:

    @staticmethod #funciona sem instancia
    #metodo que cria uma engine(conexão) a partir de um conjunto de infos vindas da página de config
    def create_engine_from_config(config):
        #pega o tipo do banco de dados
        db_type = config["db_type"]
        #ve se é sql ou postgre e a partir disso ajusta as configurações para conexão
        if db_type == "MySQL":

            url = (
                f"mysql+pymysql://"
                f"{config['user']}:"
                f"{config['password']}@"
                f"{config['host']}:"
                f"{config['port']}/"
                f"{config['database']}"
            )

        elif db_type == "PostgreSQL":

            url = (
                f"postgresql+psycopg2://"
                f"{config['user']}:"
                f"{config['password']}@"
                f"{config['host']}:"
                f"{config['port']}/"
                f"{config['database']}"
            )
        #se tiver uma opção que não tenha sido implementada retorna erro
        else:
            raise ValueError("Banco não suportado")
        #retorna a conexão
        return create_engine(url)