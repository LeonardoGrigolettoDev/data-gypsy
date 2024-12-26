# app/models/postgres.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Config

def get_postgres_engine():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    return engine

def get_postgres_session():
    engine = get_postgres_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
