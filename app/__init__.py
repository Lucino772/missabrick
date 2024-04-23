import jinja_partials
from flask import Flask
from flask_injector import FlaskInjector

from app.cli.imports import data_cli
from app.cli.user import user_cli
from app.controllers.explore import blueprint as explore_bp
from app.controllers.login import blueprint as login_bp
from app.controllers.report import blueprint as report_bp
from app.extensions import db, htmx, migrate, session
from app.inject.dao import DAOModule
from app.inject.database import DBModule
from app.inject.service import ServiceModule
from app.settings import get_config


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    jinja_partials.register_extensions(app)

    # Extensions
    db.init_app(app)
    htmx.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)

    # Blueprints
    app.register_blueprint(explore_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(report_bp)

    # CLI
    app.cli.add_command(data_cli)
    app.cli.add_command(user_cli)

    # Dependency Injection
    FlaskInjector(
        app=app,
        modules=[DBModule(app, db), DAOModule(app), ServiceModule(app)],
    )
    return app
