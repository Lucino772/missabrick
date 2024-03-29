import os
import secrets

from dotenv import load_dotenv

from app.utils import getenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def get_config():
    environment = getenv("ENVIRONMENT", "default")
    if environment == "default":
        return DefaultConfig()
    elif environment == "demo":
        return DemoConfig()
    else:
        raise RuntimeError("Invalid deployment environment")


class DefaultConfig:
    TESTING = False
    SECRET_KEY = getenv("SECRET_KEY", secrets.token_hex())
    SECURITY_PASSWORD_SALT = getenv(
        "SECURITY_PASSWORD_SALT", secrets.token_hex()
    )
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI", "sqlite:///db.sqlite3")
    SESSION_TYPE = "filesystem"
    SENDGRID_API_KEY = getenv("SENDGRID_API_KEY")
    ENABLE_DEMO_ACCOUNT = False
    DEMO_ACCOUNT_NAME = None
    DEMO_ACCOUNT_EMAIL = None
    DEMO_ACCOUNT_PASSWORD = None


class DemoConfig(DefaultConfig):
    ENABLE_DEMO_ACCOUNT = True
    DEMO_ACCOUNT_NAME = "demo"
    DEMO_ACCOUNT_EMAIL = "demo@missabrick.com"
    DEMO_ACCOUNT_PASSWORD = "demo"
