import os
import secrets

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex())
    SECURITY_PASSWORD_SALT = os.environ.get(
        "SECURITY_PASSWORD_SALT", secrets.token_hex()
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI", "sqlite:///db.sqlite3"
    )
    SESSION_TYPE = "filesystem"
