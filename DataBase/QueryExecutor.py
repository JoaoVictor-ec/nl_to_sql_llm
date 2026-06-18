from sqlalchemy import text

#classe responsável por executar queries
class QueryExecutor:

    @staticmethod # pode ser chamado sem instancia
    #metodo que recebe uma conexão e uma query e executa ela, retornando as linhas e colunas da busca
    def execute(engine, sql):
        #usa a engine e realiza a busca
        with engine.connect() as conn:

            result = conn.execute(
                text(sql)
            )

            columns = result.keys()#guarda colunas

            rows = result.fetchall()#guarda linhas

            return columns, rows