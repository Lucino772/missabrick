from flask import Blueprint

blueprint = Blueprint("catalog", __name__)

from app.catalog import models, scripts, views
