from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
