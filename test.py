from llm.OllamaClient import OllamaClient

schema_text = """
DATABASE SCHEMA

TABLE cliente
- id
- nome
- email

TABLE pedido
- id
- data
- cliente_id
"""

question = (
    "Liste todos os clientes"
)

llm = OllamaClient()

sql = llm.generate_sql(
    schema_text,
    question
)

print(sql)