from flask_compress import Compress
from flask_htmx import HTMX
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
htmx = HTMX()
compress = Compress()
migrate = Migrate()
session = Session()
