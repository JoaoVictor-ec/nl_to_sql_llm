from PySide6.QtCore import QObject, Signal

from DataBase.connection import DatabaseConnection
from DataBase.SchemaLoader import SchemaLoader

from DataBase.QueryExecutor import QueryExecutor

class SQLWorker(QObject):

    finished = Signal(object)
    error = Signal(str)

    def __init__(
        self,
        llm,
        db_config,
        question
    ):
        super().__init__()

        self.llm = llm
        self.db_config = db_config
        self.question = question

    def run(self):

        try:

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
                self.question
            )

            columns, rows = QueryExecutor.execute(
                engine,
                sql
            )

            result = {
                "sql": sql,
                "columns": columns,
                "rows": rows
            }

            self.finished.emit(result)

        except Exception as e:

            self.error.emit(str(e))