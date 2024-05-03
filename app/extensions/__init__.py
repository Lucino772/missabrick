from flask_htmx import HTMX
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from app.extensions.celery import CeleryExt
from app.extensions.proxy import ProxyFixExt

db = SQLAlchemy()
htmx = HTMX()
migrate = Migrate()
session = Session()
proxy = ProxyFixExt()
celery = CeleryExt()
