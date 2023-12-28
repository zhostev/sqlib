# app/__init__.py
from flask import Flask
from .routes import config_routes, data_routes, evaluation_routes, model_routes

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    app.register_blueprint(config_routes.bp)
    app.register_blueprint(data_routes.bp)
    app.register_blueprint(evaluation_routes.bp)
    app.register_blueprint(model_routes.bp)

    return app