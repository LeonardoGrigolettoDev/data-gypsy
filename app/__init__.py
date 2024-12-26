# app/__init__.py

from flask import Flask
from app.config import Config
from app.routes.routes import data_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Registrar blueprints
    app.register_blueprint(data_blueprint, url_prefix='/data')
    
    return app
