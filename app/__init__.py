from flask import Flask

from .routes import app_routes

def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000

    app.register_blueprint(app_routes)

    return app