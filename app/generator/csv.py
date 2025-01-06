import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
import logging
import numpy as np
from services.postgres import create_table
from models.postgres import release_connection, get_pooled_connection
# Configurar logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("import_logs.log"), logging.StreamHandler()]
)

DB_CONFIG = {
    "dbname": "seu_banco",
    "user": "seu_usuario",
    "password": "sua_senha",
    "host": "localhost",
    "port": 5432
}


def validate_csv(df):
    try:
        if df.empty:
            raise ValueError("O CSV está vazio.")
        if any(df.isnull().all()):
            raise ValueError("O CSV contém colunas completamente vazias.")
        logging.info("CSV validado com sucesso.")
    except Exception as e:
        logging.error(f"Erro na validação do CSV: {e}")
        raise


# Função para inferir tipos de dados do PostgreSQL com base no pandas
def infer_postgres_type(dtype):
    try:
        if pd.api.types.is_integer_dtype(dtype):
            return "INTEGER"
        elif pd.api.types.is_float_dtype(dtype):
            return "REAL"
        elif pd.api.types.is_bool_dtype(dtype):
            return "BOOLEAN"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            return "TIMESTAMP"
        else:
            return "TEXT"
    except Exception as e:
        logging.error(f"Erro ao inferir tipo do dado: {e}")
        raise

# Função para criar uma tabela dinamicamente
def generate_schema(csv_file, table_name):
    conn = None
    try:
        # Carregar o CSV e inferir o schema
        logging.info(f"Carregando arquivo CSV: {csv_file}")
        df = pd.read_csv(csv_file)
        validate_csv(df)
        schema = {col: infer_postgres_type(df[col]) for col in df.columns}

        # Criar tabela usando uma conexão do pool
        conn = get_pooled_connection()
        create_table(conn, table_name, schema)

        # Inserir dados em chunks
        logging.info("Iniciando inserção de dados em chunks.")
        for i, chunk in enumerate(np.array_split(df, 10)):
            try:
                insert_data(conn, table_name, chunk)
                logging.info(f"Chunk {i + 1} inserido com sucesso.")
            except Exception as e:
                logging.error(f"Erro ao inserir chunk {i + 1}: {e}")
        conn.commit()
        logging.info("Processamento do CSV finalizado com sucesso.")
    except Exception as e:
        logging.error(f"Erro geral no processamento do CSV: {e}")
    finally:
        if conn:
            release_connection(conn)


# Função para inserir dados no banco
def insert_data(table_name, data_frame):
    conn = get_pooled_connection()
    try:
        with conn.cursor() as cur:
            for _, row in data_frame.iterrows():
                columns = ", ".join(row.index)
                values = ", ".join(f"%s" for _ in row.values)
                sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                cur.execute(sql, tuple(row.values))
        conn.commit()
        logging.info(f"Dados inseridos na tabela {table_name}.")
    except Exception as e:
        logging.error(f"Erro ao inserir dados na tabela {table_name}: {e}")
        raise
    finally:
        release_connection(conn)
    # Gerar a query de inserção
    cols = list(df.columns)
    insert_query = sql.SQL("""
        INSERT INTO {table} ({columns}) VALUES %s
    """).format(
        table=sql.Identifier(table_name),
        columns=sql.SQL(", ").join(map(sql.Identifier, cols))
    )

    # Transformar DataFrame em uma lista de tuplas
    data = [tuple(row) for row in df.to_numpy()]

    # Usar execute_values para inserção em massa
    from psycopg2.extras import execute_values
    with conn.cursor() as cur:
        execute_values(cur, insert_query, data)
        conn.commit()
