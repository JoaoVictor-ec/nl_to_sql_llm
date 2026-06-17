from sqlalchemy import inspect


class SchemaLoader:

    @staticmethod
    def load_schema(engine):

        inspector = inspect(engine)

        schema = {}

        tables = inspector.get_table_names()

        for table in tables:

            columns = inspector.get_columns(table)

            schema[table] = []

            for column in columns:

                schema[table].append(
                    column["name"]
                )

        return schema

    @staticmethod
    def schema_to_text(schema):

        text = "DATABASE SCHEMA\n\n"

        for table, columns in schema.items():

            text += f"TABLE {table}\n"

            for column in columns:

                text += f"- {column}\n"

            text += "\n"

        return text