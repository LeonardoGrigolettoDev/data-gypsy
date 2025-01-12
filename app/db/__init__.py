import os
from pymongo import MongoClient


class Cli:
    ...


class MongoDB:
    def __init__(self):
        try:
            mongo_host = os.getenv("MONGO_HOST")
            mongo_port = os.getenv("MONGO_PORT")
            mongo_database = os.getenv("MONGO_DB")
            
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
        
