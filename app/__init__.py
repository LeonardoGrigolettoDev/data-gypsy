# app/__init__.py

from flask import Flask
import os
from app.db import MongoDB

def create_app():
    try:
        db = MongoDB()
    except Exception as e:
        print('Could not connect to DB:', f'{e}')
        return
    else:
        print('Connected with success:', db.check_connection())
    app = Flask(__name__)
    app.config.from_object(Config)
    from app.routes.mongo import mongo_routes
    from app.routes.routes import general_routes
    app.register_blueprint(mongo_routes, url_prefix='/db')
    app.register_blueprint(general_routes)
    return app


class Config:
    MONGO_HOST = os.getenv("MONGO_HOST")
    MONGO_DB = os.getenv("MONGO_DB")
    MONGO_PORT = os.getenv("MONGO_PORT")

