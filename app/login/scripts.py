import sqlalchemy as sa
from flask.cli import with_appcontext

from app.extensions import db
from app.login import blueprint
from app.models.user import User


@blueprint.cli.command("clear-users")
@with_appcontext
def clear_users():
    db.session.execute(sa.delete(User))
    db.session.commit()
