from flask import Flask

from app.catalog import blueprint as catalog_bp
from app.extensions import compress, db
from app.settings import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    # Extensions
    db.init_app(app)
    compress.init_app(app)

    # Blueprints
    app.register_blueprint(catalog_bp)
    return app
