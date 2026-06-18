from sqlalchemy import inspect

# classe responsável por ler o banco de dados que foi conectado e transformar em texto para llm
class SchemaLoader:

    @staticmethod
    # metodo que extrai tabelas e colunas com seus tipos do banco
    def load_schema(engine):

        #cria um explorador do bd, que le colunas, tabelas, tipos, etc
        inspector = inspect(engine)

        schema = {} # instancia uma variavel schema vazia

        tables = inspector.get_table_names() # retorna as tabelas e guarda nessa variável

        # percorre as tabelas e colunas preenchendo o schema e então retorna ele ao final
        for table in tables:

            columns = inspector.get_columns(table)

            schema[table] = []

            for column in columns:

                schema[table].append(
                    column["name"]
                )

        return schema

    @staticmethod
    # metodo que passa o schema para texto organizado
    def schema_to_text(schema):
        
        # define o que é em texto
        text = "DATABASE SCHEMA\n\n"

        # percorre o schema gerado e escreve em texto o que está presente nele de forma organizada
        for table, columns in schema.items():

            text += f"TABLE {table}\n"

            for column in columns:

                text += f"- {column}\n"

            text += "\n"

        return text