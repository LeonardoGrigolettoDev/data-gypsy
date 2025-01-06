from psycopg2 import sql
import logging
from models.postgres import get_pooled_connection, release_connection

CREATE_TABLE_QUERY_STRING = """
            CREATE TABLE IF NOT EXISTS {table} (
                {columns}
            );
        """


def create_table(table_name, schema):
    conn = get_pooled_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_QUERY_STRING)
        conn.commit()
    except Exception as e:
        logging.error(f"Erro ao criar tabela {table_name}: {e}")
        raise
    finally:
        release_connection(conn)

