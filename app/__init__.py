from flask import Flask

from app.catalog import blueprint as catalog_bp
from app.extensions import compress, db, migrate, session
from app.login import blueprint as login_bp
from app.services import sets_srv
from app.settings import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    # Extensions
    db.init_app(app)
    compress.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)

    # Services
    sets_srv.init_app(app, db)

    # Blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(catalog_bp)
    return app
