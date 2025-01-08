import psycopg2
import os
from pymongo import MongoClient
from app import config


class Cli:
    ...

class PostgreSQL:
    def __init__(self):
        try:
            # Carregar as variáveis de ambiente
            self.conn = psycopg2.connect(
                database=config.POSTGRES_DB,
                user=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD,
                host=config.POSTGRES_HOST,
                port=config.POSTGRES_PORT
            )
            self.cursor = self.conn.cursor()
        except psycopg2.OperationalError as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {str(e)}")
    

    def get_all(self, table_name):
        """Obtém todos os registros de uma tabela."""
        query = f'SELECT * FROM "tab{table_name}";'
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao executar get_all: {e}")
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def get_by_id(self, table_name, record_id):
        """Obtém um registro pelo ID."""
        query = f"SELECT * FROM {table_name} WHERE id = %s;"
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (record_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao executar get_by_id: {e}")
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def delete(self, table_name, record_id):
        """Exclui um registro pelo ID."""
        query = f"DELETE FROM {table_name} WHERE id = %s;"
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (record_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao executar delete: {e}")
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def insert(self, table_name, data: dict):
        """Insere um novo registro."""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING id;"
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, tuple(data.values()))
            new_id = cursor.fetchone()["id"]
            self.conn.commit()
            return new_id
        except Exception as e:
            print(f"Erro ao executar insert: {e}")
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def update(self, table_name, record_id, data: dict):
        """Atualiza um registro."""
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE id = %s;"
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (*data.values(), record_id))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao executar update: {e}")
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def create_table(self, table_name, schema: dict):
        """
        Cria uma nova tabela com base em um esquema fornecido.
        :param table_name: Nome da tabela.
        :param schema: Dicionário onde as chaves são nomes de colunas e os valores são os tipos de dados SQL.
        """
        columns = ', '.join([f"{col} {dtype}" for col, dtype in schema.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao executar create_table: {e}")
            self.conn.rollback()
            raise
        finally:
            print(f'Table {table_name} created.')
            cursor.close()

    def bulk_update(self, table_name, updates: list):
        """
        Realiza atualizações em massa em uma tabela.
        :param table_name: Nome da tabela.
        :param updates: Lista de dicionários, cada um contendo 'id' e as colunas a serem atualizadas.
        """
        cursor = self.conn.cursor()
        try:
            for update in updates:
                record_id = update.pop('id', None)
                if not record_id:
                    raise ValueError("Cada atualização deve conter um 'id'")
                set_clause = ', '.join([f"{key} = %s" for key in update.keys()])
                query = f"UPDATE {table_name} SET {set_clause} WHERE id = %s;"
                cursor.execute(query, (*update.values(), record_id))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao executar bulk_update: {e}")
            self.conn.rollback()
            raise
        finally:
            cursor.close()
    def check_connection(self):
        try:
            # Executando uma consulta simples para verificar a conexão
            self.cursor.execute("SELECT 1")
            return True
        except Exception as e:
            return False


class MongoDB:
    def __init__(self):
        try:
            mongo_host = config.MONGO_HOST
            mongo_port = config.MONGO_PORT
            mongo_database = config.MONGO_DB
            
            # Conectando ao MongoDB
            self.client = MongoClient(mongo_host, int(mongo_port))
            self.db = self.client[mongo_database]
        except Exception as e:
            raise Exception(f"Erro ao conectar ao MongoDB: {str(e)}")

    def get_all(self, collection_name):
        """Obtém todos os documentos de uma coleção."""
        try:
            collection = self.db[collection_name]
            return list(collection.find())
        except Exception as e:
            print(f"Erro ao executar get_all: {e}")
            raise

    def get_by_id(self, collection_name, record_id):
        """Obtém um documento pelo ID."""
        try:
            collection = self.db[collection_name]
            return collection.find_one({"_id": record_id})
        except Exception as e:
            print(f"Erro ao executar get_by_id: {e}")
            raise

    def delete(self, collection_name, record_id):
        """Exclui um documento pelo ID."""
        try:
            collection = self.db[collection_name]
            result = collection.delete_one({"_id": record_id})
            return result.deleted_count
        except Exception as e:
            print(f"Erro ao executar delete: {e}")
            raise

    def insert(self, collection_name, data):
        """Insere um novo documento."""
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            print(f"Erro ao executar insert: {e}")
            raise

    def update(self, collection_name, record_id, data):
        """Atualiza um documento."""
        try:
            collection = self.db[collection_name]
            result = collection.update_one({"_id": record_id}, {"$set": data})
            return result.modified_count
        except Exception as e:
            print(f"Erro ao executar update: {e}")
            raise

    def create_collection(self, collection_name):
        """Cria uma nova coleção se ela não existir."""
        try:
            if collection_name not in self.db.list_collection_names():
                self.db.create_collection(collection_name)
            return True
        except Exception as e:
            print(f"Erro ao criar coleção: {e}")
            raise

    def bulk_update(self, collection_name, updates: list):
        """
        Realiza atualizações em massa em uma coleção.
        :param collection_name: Nome da coleção.
        :param updates: Lista de dicionários, cada um contendo '_id' e os campos a serem atualizados.
        """
        try:
            collection = self.db[collection_name]
            for update in updates:
                record_id = update.pop("_id", None)
                if not record_id:
                    raise ValueError("Cada atualização deve conter um '_id'")
                collection.update_one({"_id": record_id}, {"$set": update})
            return True
        except Exception as e:
            print(f"Erro ao executar bulk_update: {e}")
            raise

    def check_connection(self):
        try:
            self.client.server_info()
            return True
        except Exception as e:
            return False
        
