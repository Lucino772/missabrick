from flask import Flask

from app.cli.imports import data_cli
from app.cli.user import user_cli
from app.controllers.explore import blueprint as explore_bp
from app.controllers.login import blueprint as login_bp
from app.controllers.report import blueprint as report_bp
from app.extensions import compress, db, migrate, session
from app.factories import teardown_dao_factory, teardown_service_factory
from app.factory.dao import DaoFactory
from app.factory.service import ServiceFactory
from app.settings import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    # Extensions
    db.init_app(app)
    compress.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)

    # Blueprints
    app.register_blueprint(explore_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(report_bp)

    # CLI
    app.cli.add_command(data_cli)
    app.cli.add_command(user_cli)

    # Service Factory
    app.service_factory_class = ServiceFactory
    app.teardown_appcontext(teardown_service_factory)

    # Dao Factory
    app.dao_factory_class = DaoFactory
    app.teardown_appcontext(teardown_dao_factory)

    return app
