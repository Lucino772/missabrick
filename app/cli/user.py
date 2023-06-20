import sqlalchemy as sa
from flask.cli import AppGroup, with_appcontext

from app.extensions import db
from app.models.orm.login import User

user_cli = AppGroup("user")


@user_cli.command("clear")
@with_appcontext
def clear_users():
    db.session.execute(sa.delete(User))
    db.session.commit()
