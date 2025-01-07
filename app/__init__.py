# app/__init__.py

from flask import Flask
from app.config import Config


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
