from sqlalchemy import create_engine


class DatabaseConnection:

    @staticmethod
    def create_engine_from_config(config):

        db_type = config["db_type"]

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

        else:
            raise ValueError("Banco não suportado")

        return create_engine(url)