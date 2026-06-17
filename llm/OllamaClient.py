from ollama import chat


class OllamaClient:

    def __init__(self, model="qwen3:14b"):

        self.model = model

    def ask(self, prompt):

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    def generate_sql(
        self,
        schema_text,
        question
    ):

        prompt = f"""
Você é um especialista em SQL.

Utilize SOMENTE as tabelas e colunas fornecidas.

{schema_text}

Pergunta:
{question}

Regras:

1. Gere apenas SQL.
2. Não explique.
3. Não use markdown.
4. Não use ```sql.
5. Retorne apenas um comando SQL válido.
"""

        return self.ask(prompt)