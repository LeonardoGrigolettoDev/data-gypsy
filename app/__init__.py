# app/__init__.py

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from app.routes.mongo import mongo_routes
    from app.routes.postgres import postgres_routes
    from app.routes.routes import general_routes
    app.register_blueprint(mongo_routes, url_prefix='/mongo')
    app.register_blueprint(postgres_routes, url_prefix='/postgres')
    app.register_blueprint(general_routes)
    return app

import os

class Config:
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_ROOT_USER = os.getenv("POSTGRES_ROOT_USER")
    POSTGRES_ROOT_PASSWORD = os.getenv("POSTGRES_ROOT_PASSWORD")
    MONGO_HOST = os.getenv("MONGO_HOST")
    MONGO_DB = os.getenv("MONGO_DB")
    MONGO_PORT = os.getenv("MONGO_PORT")

config = Config()
