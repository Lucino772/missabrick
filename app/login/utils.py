import sqlalchemy as sa

from app.extensions import db
from app.login.models import User


class UsernameAlreadyTaken(Exception):
    pass


class EmailAlreadyTaken(Exception):
    pass


class ConfirmPasswordDoesNotMatch(Exception):
    pass


def get_user():
    pass


def create_user(username: str, email: str, password: str):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()


def check_username(name: str):
    user = db.session.execute(
        sa.select(User).filter(User.username == name)
    ).scalar_one()

    if user is not None:
        raise UsernameAlreadyTaken()


def check_email(email: str):
    user = db.session.execute(
        sa.select(User).filter(User.email == email)
    ).scalar_one()

    if user is not None:
        raise EmailAlreadyTaken()


def check_confirm_password(password: str, confirm: str):
    if password != confirm:
        raise ConfirmPasswordDoesNotMatch()
