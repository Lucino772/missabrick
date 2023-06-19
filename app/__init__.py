from flask import Flask

from app.extensions import compress, db, migrate, session
from app.settings import Config
from app.views.explore import ExploreView
from app.views.login import LoginView
from app.views.report import ReportView


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    # Extensions
    db.init_app(app)
    compress.init_app(app)
    migrate.init_app(app, db)
    session.init_app(app)

    # Blueprints
    app.register_blueprint(LoginView().as_blueprint())
    app.register_blueprint(ExploreView().as_blueprint())
    app.register_blueprint(ReportView().as_blueprint())

    return app
