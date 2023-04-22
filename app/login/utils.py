import datetime as dt
import os

import itsdangerous
import sendgrid
import sqlalchemy as sa
from flask import current_app
from sendgrid.helpers.mail import Content, Email, Mail, To
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


class EmailVerificationError(Exception):
    def __init__(
        self, *args: object, timeout: bool = False, invalid_email: bool = False
    ) -> None:
        super().__init__(*args)
        self.timeout = timeout
        self.invalid_email = invalid_email


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


def generate_verify_mail_token(email: str):
    serializer = itsdangerous.URLSafeTimedSerializer(
        secret_key=current_app.config["SECRET_KEY"],
        salt=current_app.config["SECURITY_PASSWORD_SALT"],
    )
    return serializer.dumps(email)


def confirm_verify_mail_token(token: str, expiration: int = 3600):
    serializer = itsdangerous.URLSafeTimedSerializer(
        secret_key=current_app.config["SECRET_KEY"],
        salt=current_app.config["SECURITY_PASSWORD_SALT"],
    )
    try:
        email = serializer.loads(token, max_age=expiration)
        user: User = db.session.execute(
            sa.select(User).filter(User.email == email)
        ).scalar_one()
        user.email_verified = True
        user.email_verified_on = dt.datetime.now()
        db.session.add(user)
        db.session.commit()
    except itsdangerous.SignatureExpired:
        raise EmailVerificationError(timeout=True)
    except itsdangerous.BadSignature:
        raise EmailVerificationError()
    except NoResultFound:
        raise EmailVerificationError(invalid_email=True)


def send_verify_mail(dest_email: str, link: str):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))

    from_email = Email("noreply-missabrick@lucapalmi.com")
    subject = "MissABrick - Verify your email"
    content = Content(
        "text/plain",
        f"You can verify your email by clicking on this link: {link}",
    )
    mail = Mail(from_email, To(dest_email), subject, content)
    mail_json = mail.get()
    sg.send(mail_json)
