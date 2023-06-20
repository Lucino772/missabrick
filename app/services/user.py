import datetime as dt
import typing as t

import itsdangerous
import sqlalchemy as sa
from flask import current_app, url_for

from app.errors import (
    EmailVerificationError,
    InvalidEmailOrPassword,
    PasswordDoesNotMatch,
    UserAlreadyExists,
)
from app.extensions import db
from app.interfaces.services.user import IUserService
from app.models.orm.login import User

if t.TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from app.services.mail import MailService

_sentinel = object()


def _get_dangerous_serializer():
    return itsdangerous.URLSafeTimedSerializer(
        secret_key=current_app.config["SECRET_KEY"],
        salt=current_app.config["SECURITY_PASSWORD_SALT"],
    )


class UserService(IUserService):
    __slots__ = ("db", "session", "mail_srv")

    def __init__(self, mail_srv: "MailService" = None) -> None:
        self.db = db
        self.session: "Session" = db.session
        self.mail_srv = mail_srv

    def _user_exists(self, email: str = _sentinel, username: str = _sentinel):
        conditions = []
        if email is not _sentinel:
            conditions.append(User.email == email)
        if username is not _sentinel:
            conditions.append(User.username == username)

        if len(conditions) == 0:
            return False

        query = sa.select(User).where(sa.or_(*conditions))
        return self.session.execute(query).scalars().first() is not None

    def _get_user_by_email(self, email: str):
        return self.session.execute(
            sa.select(User).filter(User.email == email)
        ).scalar_one_or_none()

    def create_user(
        self, username: str, email: str, password: str, confirm: str
    ):
        if password != confirm:
            raise PasswordDoesNotMatch()

        if self._user_exists(email, username):
            raise UserAlreadyExists()

        user = User(username=username, email=email, password=password)
        self.session.add(user)
        self.session.commit()

        # Send email confirmation link
        token = _get_dangerous_serializer().dumps(user.email)
        verify_link = url_for(
            "login.verify_email", token=token, _external=True
        )
        self.mail_srv.send(
            _from="noreply-missabrick@lucapalmi.com",
            to=user.email,
            subject="MissABrick - Verify your email",
            content=f"You can verify your email by clicking on this link: {verify_link}",
        )

        return user

    def check_password(self, email: str, password: str):
        user = self._get_user_by_email(email)
        if user is None or user.password != password:
            raise InvalidEmailOrPassword()

    def verify_email(self, token: str, expiration: int = 3600):
        try:
            email = _get_dangerous_serializer().loads(
                token, max_age=expiration
            )
            user = self._get_user_by_email(email)
            if user is None:
                raise EmailVerificationError(invalid_email=True)

            user.email_verified = True
            user.email_verified_on = dt.datetime.now()
            self.session.add(user)
            self.session.commit()
        except itsdangerous.SignatureExpired:
            raise EmailVerificationError(timeout=True)
        except itsdangerous.BadSignature:
            raise EmailVerificationError()
