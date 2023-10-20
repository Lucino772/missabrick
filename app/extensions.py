from flask_compress import Compress
from flask_htmx import HTMX
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_session import Session

db = SQLAlchemy()
htmx = HTMX()
compress = Compress()
migrate = Migrate()
session = Session()
