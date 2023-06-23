import datetime as dt

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


@user_cli.command("demo")
@with_appcontext
def create_demo_user():
    user = User(
        username="demo",
        email="demo@missabrick.com",
        password="demo",
        email_verified=True,
        email_verified_on=dt.datetime.now(),
    )
    db.session.add(user)
    db.session.commit()
