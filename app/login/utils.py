import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound

from app.extensions import db
from app.login.models import User


class UsernameAlreadyTaken(Exception):
    pass


class EmailAlreadyTaken(Exception):
    pass


class ConfirmPasswordDoesNotMatch(Exception):
    pass


class LoginError(Exception):
    pass


def check_login(email: str, password: str):
    try:
        user = db.session.execute(
            sa.select(User).filter(User.email == email)
        ).scalar_one()
        if user.password != password:
            raise LoginError()
    except NoResultFound:
        raise LoginError()


def create_user(username: str, email: str, password: str):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()


def check_username(name: str):
    try:
        user = db.session.execute(
            sa.select(User).filter(User.username == name)
        ).scalar_one()

        if user is not None:
            raise UsernameAlreadyTaken()
    except NoResultFound:
        pass


def check_email(email: str):
    try:
        user = db.session.execute(
            sa.select(User).filter(User.email == email)
        ).scalar_one()

        if user is not None:
            raise EmailAlreadyTaken()
    except NoResultFound:
        pass


def check_confirm_password(password: str, confirm: str):
    if password != confirm:
        raise ConfirmPasswordDoesNotMatch()
