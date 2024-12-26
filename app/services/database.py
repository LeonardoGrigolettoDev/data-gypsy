from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['data_db']
collection = db['xml_data']

def save_to_mongodb(data):
    collection.insert_one(data)
