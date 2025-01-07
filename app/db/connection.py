import psycopg2
from psycopg2.extras import RealDictCursor
from pymongo import MongoClient


class Connection:
    def __init__(self, db_type: str, host: str, database: str, user: str = None, password: str = None, port: int = None):
        """
        Inicializa a conexão com base no tipo do banco (PostgreSQL ou MongoDB).

        :param db_type: Tipo de banco de dados ("postgresql" ou "mongodb").
        :param host: Host do banco de dados.
        :param database: Nome do banco de dados.
        :param user: Nome de usuário (necessário para PostgreSQL).
        :param password: Senha (necessário para PostgreSQL).
        :param port: Porta do banco de dados.
        """
        self.db_type = db_type.lower()
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
            if self.db_type == "postgresql":
                self.conn = psycopg2.connect(**self.connection_params)
            elif self.db_type == "mongodb":
                uri = f"mongodb://{self.connection_params['host']}:{self.connection_params['port']}/"
                self.conn = MongoClient(uri)[self.connection_params["database"]]
            else:
                raise ValueError("Tipo de banco de dados não suportado. Use 'postgresql' ou 'mongodb'.")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados ({self.db_type}): {e}")
            raise

    def get_cursor(self):
        """Retorna um cursor para executar consultas (apenas para PostgreSQL)."""
        if self.db_type != "postgresql":
            raise ValueError("O método 'get_cursor' é válido apenas para PostgreSQL.")
        if not self.conn:
            self.connect()
        return self.conn.cursor(cursor_factory=RealDictCursor)

    def get_collection(self, collection_name):
        """Retorna uma coleção para executar operações (apenas para MongoDB)."""
        if self.db_type != "mongodb":
            raise ValueError("O método 'get_collection' é válido apenas para MongoDB.")
        if not self.conn:
            self.connect()
        return self.conn[collection_name]

    def close(self):
        """Fecha a conexão com o banco."""
        if self.conn:
            if self.db_type == "postgresql":
                self.conn.close()
            elif self.db_type == "mongodb":
                self.conn.client.close()
