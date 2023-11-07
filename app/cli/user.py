import datetime as dt

import sqlalchemy as sa
from flask import current_app
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
    if current_app.config["ENABLE_DEMO_ACCOUNT"]:
        user_exists = (
            db.session.execute(
                sa.select(User).where(
                    User.email == current_app.config["DEMO_ACCOUNT_EMAIL"]
                )
            )
            .scalars()
            .first()
            is not None
        )

        if not user_exists:
            user = User(
                username=current_app.config["DEMO_ACCOUNT_NAME"],
                email=current_app.config["DEMO_ACCOUNT_EMAIL"],
                password=current_app.config["DEMO_ACCOUNT_PASSWORD"],
                email_verified=True,
                email_verified_on=dt.datetime.now(),
            )
            db.session.add(user)
            db.session.commit()
            print("Added demo account")
        else:
            print("Demo user exists")
    else:
        print("Demo account not enabled")
