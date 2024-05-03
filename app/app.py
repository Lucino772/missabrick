import jinja_partials
from cachelib import FileSystemCache
from celery.schedules import crontab
from flask import Flask
from flask_injector import FlaskInjector

from app.cli.imports import data_cli
from app.cli.user import user_cli
from app.config import AppConfig
from app.controllers.explore import blueprint as explore_bp
from app.controllers.login import blueprint as login_bp
from app.controllers.report import blueprint as report_bp
from app.extensions import celery, db, htmx, migrate, proxy, session
from app.inject.dao import DAOModule
from app.inject.database import DBModule
from app.inject.service import ServiceModule
from app.tasks.rebrickable import import_data


def create_app():
    # Workaround for issue with Flask-Injector, see:
    # https://github.com/python-injector/flask_injector/issues/78
    Flask.url_for.__annotations__ = {}

    app = Flask(__name__)
    app.config.from_object(AppConfig())
    jinja_partials.register_extensions(app)

    # Session Configuration
    app.config["SESSION_TYPE"] = "cachelib"
    app.config["SESSION_CACHELIB"] = FileSystemCache(
        cache_dir="flask_session", threshold=100
    )

    # Extensions
    db.init_app(app)
    htmx.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)
    proxy.init_app(app)

    # Configure Periodic Tasks
    celery_app = celery.init_app(app)
    celery_app.conf.beat_schedule = {
        "import_data_from_rebrickable": {
            "task": import_data.s().name,
            "schedule": crontab(minute="*/30"),
        }
    }

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
