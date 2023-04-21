import secrets

from flask import Flask

from app.catalog import blueprint as catalog_bp
from app.extensions import compress, db


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex()

    # SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    db.init_app(app)

    # flask-compress
    compress.init_app(app)

    # Blueprints
    app.register_blueprint(catalog_bp)
    return app
