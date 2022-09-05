from flask import Flask
from config import config

from app.database import SQLiteDatabase
from app.database.sqlite import SQLiteCLI

db = SQLiteDatabase('./db-dev.sqlite')
db_cli = SQLiteCLI('./db-dev.sqlite')

def create_app(config_name: str):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
