from flask import Blueprint

blueprint = Blueprint('catalog', __name__)

from app.catalog import views
from app.catalog import models
from app.catalog import scripts