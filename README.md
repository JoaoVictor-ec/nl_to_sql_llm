# NL to SQL – Natural Language to SQL Converter

Sistema de conversão de linguagem natural para SQL utilizando LLM local (Ollama), com execução em bancos MySQL e PostgreSQL e interface gráfica em PySide6.

---

## Funcionalidades

- Conexão com MySQL e PostgreSQL  
- Extração automática do schema do banco  
- Interface gráfica para consultas em linguagem natural  
- Geração de SQL via LLM (Ollama)  
- Execução da query no banco  
- Exibição dos resultados em tabela  
- Interface responsiva com processamento em thread  

---

## Arquitetura do Sistema

Fluxo de execução:

Usuário (linguagem natural)
↓
Interface PySide6 (MainWindow)
↓
SQLWorker (Thread separada)
↓
SchemaLoader (extrai estrutura do banco)
↓
Ollama LLM (gera SQL)
↓
QueryExecutor (executa SQL)
↓
Banco de dados
↓
Interface exibe resultados

---

## Bibliotecas utilizadas

- Python 3
- PySide6  
- SQLAlchemy  
- Ollama  
- PyMySQL  
- psycopg2-binary  
- Pandas  

---

## Instalação

### 1. Clonar o repositório

git clone <https://github.com/JoaoVictor-ec/nl_to_sql_llm>
cd <nl_to_sql_llm>

---

### 2. Criar ambiente virtual (Linux)

python3 -m venv nl_sql

---

### 3. Ativar ambiente virtual (Linux)

source nl_sql/bin/activate

---

### 4. Instalar dependências

pip install ollama  
pip install sqlalchemy  
pip install pymysql  
pip install psycopg2-binary  
pip install pandas  
pip install pyside6  

---

### 5. Instalar e iniciar o Ollama

https://ollama.com/

ollama pull qwen3:14b

---

## Como executar

python main.py

---

## Como usar

1. Clique em Configurar Banco  
2. Escolha MySQL ou PostgreSQL  
3. Insira host, porta, usuário e senha  
4. Teste a conexão e salve
5. Escreva uma pergunta em linguagem natural  

Ex: Quais clientes fizeram mais pedidos?

6. Clique em Consultar (pode demorar alguns segundos dependendo da complexiadade da consulta)
7. O sistema irá:
   - gerar SQL automaticamente  
   - executar no banco  
   - exibir resultado na tabela  

---


## Estrutura do projeto

gui/  
llm/  
DataBase/  
main.py  

---

## Ambiente de desenvolvimento

Projeto desenvolvido no seguinte ambiente:

- Sistema operacional: Ubuntu 22.04 LTS  
- CPU: 16 GB RAM  
- GPU: NVIDIA RTX 4050 (6 GB VRAM)  
- Python 3.x  
- Execução em ambiente virtual (venv: nl_sql)  

---

## Autor

João Victor Mendes de Siqueira – Disciplina: Introdução a bancos de dados.
