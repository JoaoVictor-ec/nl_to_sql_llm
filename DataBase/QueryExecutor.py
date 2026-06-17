from sqlalchemy import text


class QueryExecutor:

    @staticmethod
    def execute(engine, sql):

        with engine.connect() as conn:

            result = conn.execute(
                text(sql)
            )

            columns = result.keys()

            rows = result.fetchall()

            return columns, rows