from PySide6.QtCore import QObject, Signal

from DataBase.connection import DatabaseConnection
from DataBase.SchemaLoader import SchemaLoader

from DataBase.QueryExecutor import QueryExecutor

# classe responsável por rodar o pipeline de resposta fora da UI para evitar congelamentos e possíveis travas no python
class SQLWorker(QObject):

    # emite um sinal (objeto que dispara mensagem para o que estiver conectado) caso funcione, passando então os resultado ou então emite sinal de erro
    finished = Signal(object)
    error = Signal(str)

    #insere as dependencias que serão necessárias
    def __init__(
        self,
        llm,
        db_config,
        question
    ):
        super().__init__()
        
        # guarda o modelo de llm, a config do bd e a pergunta do usuário
        self.llm = llm
        self.db_config = db_config
        self.question = question
    
    # executa o pipeline
    def run(self):

        try:
            
            #estabelece conexão usando as configs, faz isso via sqlAlchemy
            engine = (
                DatabaseConnection
                .create_engine_from_config(
                    self.db_config
                )
            )

            # pega o schema do banco, extraindo as tabelas colunas e seus tipos. 
            schema = (
                SchemaLoader
                .load_schema(engine)
            )

            # passa o schema para texto
            schema_text = (
                SchemaLoader
                .schema_to_text(schema)
            )

            # manda para llm os textos de esquema do bd e pergunta do usuário e guarda a resposta do sql
            sql = self.llm.generate_sql(
                schema_text,
                self.question
            )

            # executa a query obtida da llm
            columns, rows = QueryExecutor.execute(
                engine,
                sql
            )

            # monta o resultado que deverá ser mostrado
            result = {
                "sql": sql,
                "columns": columns,
                "rows": rows
            }

            #emite o sinal de finalização
            self.finished.emit(result)

        # em caso de erro, apenas retorna sinal de erro
        except Exception as e:

            self.error.emit(str(e))