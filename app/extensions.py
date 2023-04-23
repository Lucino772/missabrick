from flask_compress import Compress
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
compress = Compress()
migrate = Migrate()
session = Session()
