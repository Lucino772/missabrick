import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex())
    MAX_CONTENT_LENGTH = 100000 # 100 KB

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}