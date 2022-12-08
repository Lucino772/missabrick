import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex())
    MAX_CONTENT_LENGTH = 100000 # 100 KB
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db-dev.sqlite'))

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}