import os
from pymongo import MongoClient

mongo_host = os.getenv("MONGO_HOST", "localhost")
mongo_port = os.getenv("MONGO_PORT", "27017")
mongo_user = os.getenv("MONGO_ROOT_USERNAME", "admin")
mongo_pass = os.getenv("MONGO_ROOT_PASSWORD", "password")
mongo_database = os.getenv("MONGO_DB", "mongodb")
mongo_collection = "User"

conn = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/?authSource=admin"
client = MongoClient(conn)

db = client[mongo_database]
if mongo_collection not in db.list_collection_names():
    db.create_collection(mongo_collection)

db[mongo_collection].insert_one({
    "username": os.getenv("MONGO_ROOT_USERNAME", "admin"),
    "password": os.getenv("MONGO_ROOT_PASSWORD", "password"),
    "role": "root"
})
