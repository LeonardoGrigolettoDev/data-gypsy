# app/models/postgres.py

import psycopg2
import logging
from models import DB_CONFIG

from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **DB_CONFIG
)

def get_pooled_connection():
    try:
        conn = connection_pool.getconn()
        logging.info("Conexão adquirida do pool.")
        return conn
    except Exception as e:
        logging.error(f"Erro ao adquirir conexão do pool: {e}")
        raise

def release_connection(conn):
    try:
        connection_pool.putconn(conn)
        logging.info("Conexão devolvida ao pool.")
    except Exception as e:
        logging.error(f"Erro ao devolver conexão ao pool: {e}")
        