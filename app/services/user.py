import datetime as dt

import itsdangerous
from flask import current_app, url_for

from app.errors import (
    EmailVerificationError,
    InvalidEmailOrPassword,
    PasswordDoesNotMatch,
    UserAlreadyExists,
)
from app.factories import dao_factory
from app.interfaces.factory.service import IServiceFactory
from app.interfaces.services.user import IUserService
from app.models.orm.login import User
from app.services.abstract import AbstractService


def _get_dangerous_serializer():
    return itsdangerous.URLSafeTimedSerializer(
        secret_key=current_app.config["SECRET_KEY"],
        salt=current_app.config["SECURITY_PASSWORD_SALT"],
    )


class UserService(AbstractService, IUserService):
    __slots__ = ("user_dao", "mail_srv")

    def __init__(self, factory: IServiceFactory) -> None:
        super().__init__(factory)
        self.user_dao = dao_factory.get_user_dao()
        self.mail_srv = self.service_factory.get_mail_service()

    def create_user(
        self, username: str, email: str, password: str, confirm: str
    ):
        if password != confirm:
            raise PasswordDoesNotMatch()

        if self.user_dao.exists(email, username):
            raise UserAlreadyExists()

        user = User(username=username, email=email, password=password)
        self.user_dao.save(user)

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
        user = self.user_dao.get_by_email(email)
        if user is None or user.password != password:
            raise InvalidEmailOrPassword()

    def verify_email(self, token: str, expiration: int = 3600):
        try:
            email = _get_dangerous_serializer().loads(
                token, max_age=expiration
            )
            user = self.user_dao.get_by_email(email)
            if user is None:
                raise EmailVerificationError(invalid_email=True)

            user.email_verified = True
            user.email_verified_on = dt.datetime.now()
            self.user_dao.save(user)
        except itsdangerous.SignatureExpired:
            raise EmailVerificationError(timeout=True)
        except itsdangerous.BadSignature:
            raise EmailVerificationError()
