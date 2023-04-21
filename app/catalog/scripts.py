from app.database import db
from app.catalog import blueprint

from flask.cli import with_appcontext

@blueprint.cli.command("create-db")
@with_appcontext
def createdb():
    db.create_all()
