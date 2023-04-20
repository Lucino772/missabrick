from flask import Flask

from app.catalog import blueprint as catalog_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(catalog_bp)
    return app
