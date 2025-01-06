from psycopg2 import sql
from psycopg2.extras import execute_values
from models.postgres import get_connection
from generator.db import create_table
from generator.csv import validate_csv, infer_postgres_type
import pandas as pd
import logging

def insert_data(conn, table_name, df):
    try:
        data = [tuple(row) for row in df.to_numpy()]
        insert_query = sql.SQL("""
            INSERT INTO {table} ({columns}) VALUES %s
        """).format(
            table=sql.Identifier(table_name),
            columns=sql.SQL(", ").join(map(sql.Identifier, df.columns))
        )
        with conn.cursor() as cur:
            execute_values(cur, insert_query, data)
            conn.commit()
        logging.info(f"Dados inseridos com sucesso na tabela '{table_name}'.")
    except Exception as e:
        logging.error(f"Erro ao inserir dados na tabela '{table_name}': {e}")
        raise

def process_csv_resilient(csv_file, table_name, chunksize=1000):
    errored_chunks = []
    try:
        conn = get_connection()
        for i, chunk in enumerate(pd.read_csv(csv_file, chunksize=chunksize)):
            try:
                insert_data(conn, table_name, chunk)
            except Exception as e:
                logging.error(f"Erro no chunk {i}: {e}")
                errored_chunks.append(i)
        
        if errored_chunks:
            logging.warning(f"Chunks com erro: {errored_chunks}")
    except Exception as e:
        logging.error(f"Erro crítico no processamento: {e}")
    finally:
        conn.close()
# def process_csv_to_postgres(csv_file, table_name):
#     try:
#         logging.info(f"Iniciando processamento do arquivo: {csv_file}")
        
#         # Carregar CSV
#         df = pd.read_csv(csv_file)
#         validate_csv(df)
        
#         # Inferir schema
#         schema = {col: infer_postgres_type(df[col]) for col in df.columns}
#         logging.info(f"Schema inferido: {schema}")
        
#         # Conectar ao banco
#         conn = get_connection()
        
#         # Criar tabela e inserir dados
#         create_table(conn, table_name, schema)
#         insert_data(conn, table_name, df)
        
#         logging.info("Processamento finalizado com sucesso.")
#     except Exception as e:
#         logging.error(f"Erro no processamento do CSV: {e}")
#         raise
#     finally:
#         try:
#             conn.close()
#             logging.info("Conexão com o banco encerrada.")
#         except:
#             pass
def process_csv_in_chunks(csv_file, table_name, chunksize=1000):
    try:
        logging.info(f"Iniciando processamento em chunks para o arquivo: {csv_file}")
        conn = get_connection()
        
        for chunk in pd.read_csv(csv_file, chunksize=chunksize):
            validate_csv(chunk)  # Validar cada chunk
            schema = {col: infer_postgres_type(chunk[col]) for col in chunk.columns}
            
            # Criar tabela apenas na primeira iteração
            if chunk.index[0] == 0:
                create_table(conn, table_name, schema)
            
            insert_data(conn, table_name, chunk)  # Inserir dados chunk a chunk
        
        logging.info("Processamento em chunks finalizado com sucesso.")
    except Exception as e:
        logging.error(f"Erro no processamento em chunks: {e}")
        raise
    finally:
        try:
            conn.close()
            logging.info("Conexão com o banco encerrada.")
        except:
            pass