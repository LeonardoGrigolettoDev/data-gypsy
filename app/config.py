# app/config.py

class Config:
    # MongoDB Configuration
    MONGO_URI = "mongodb://root:password@localhost:27017/my_database"
    
    # PostgreSQL Configuration
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost:5432/my_database"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Kafka Configuration
    KAFKA_BROKER_URL = "localhost:9092"
