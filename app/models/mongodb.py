# app/models/mongodb.py

from pymongo import MongoClient
from app.config import Config

client = MongoClient('mongodb://localhost:27017/')
db = client['data_db']
collection = db['xml_data']

def get_mongo_client():
    client = MongoClient(Config.MONGO_URI)
    return client

def get_mongo_db():
    client = get_mongo_client()
    db = client["my_database"]  # Nome do banco
    return db

def save_to_mongodb(data):
    collection.insert_one(data)