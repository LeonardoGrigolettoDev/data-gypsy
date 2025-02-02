# app/__init__.py

from flask import Flask
import os
from app.setup import setup_tables
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from app.routes.routes import general_routes
    app.register_blueprint(general_routes)
    setup_tables()
    return app

