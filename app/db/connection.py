import psycopg2
from psycopg2.extras import RealDictCursor
from pymongo import MongoClient


class Connection:
    def __init__(self, host: str, database: str, user: str = None, password: str = None, port: int = None):
        """
        Inicializa a conexão com base no tipo do banco (PostgreSQL ou MongoDB).

        :param db_type: Tipo de banco de dados ("postgresql" ou "mongodb").
        :param host: Host do banco de dados.
        :param database: Nome do banco de dados.
        :param user: Nome de usuário (necessário para PostgreSQL).
        :param password: Senha (necessário para PostgreSQL).
        :param port: Porta do banco de dados.
        """
        self.connection_params = {
            "host": host,
            "database": database,
            "user": user,
            "password": password,
            "port": port,
        }
        self.conn = None

    def connect(self):
        """Estabelece a conexão com o banco de dados."""
        try:
            uri = f"mongodb://{self.connection_params['host']}:{
                self.connection_params['port']}/"
            self.conn = MongoClient(uri)[self.connection_params["database"]]
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados ({self.db_type}): {e}")
            raise

    def get_collection(self, collection_name):
        """Retorna uma coleção para executar operações (apenas para MongoDB)."""
        if not self.conn:
            self.connect()
        return self.conn[collection_name]

    def close(self):
        """Fecha a conexão com o banco."""
        if self.conn:
            self.conn.client.close()
