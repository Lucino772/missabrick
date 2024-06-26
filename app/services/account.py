import datetime as dt

import itsdangerous
from flask import url_for
from injector import inject

from app.errors import (
    EmailVerificationError,
    PasswordDoesNotMatchError,
    UserAlreadyExistsError,
)
from app.interfaces.daos.user import IUserDao
from app.interfaces.services.mail import IMailService
from app.interfaces.services.signing import ISigningService
from app.models.orm.login import User


@inject
class AccountService:
    def __init__(
        self,
        user_dao: IUserDao,
        signing_service: ISigningService,
        mail_service: IMailService,
    ) -> None:
        self.user_dao = user_dao
        self.signing_service = signing_service
        self.mail_service = mail_service

    def create_account(
        self, username: str, email: str, password: str, confirm: str
    ) -> User:
        if password != confirm:
            raise PasswordDoesNotMatchError

        if self.user_dao.exists(email, username):
            raise UserAlreadyExistsError

        user = User(username=username, email=email, password=password)
        self.user_dao.save(user)

        # Send email confirmation link
        token = self.signing_service.urlsafe_dumps(user.email)
        verify_link = url_for("login.verify_email", token=token, _external=True)
        self.mail_service.send(
            _from="noreply-missabrick@lucapalmi.com",
            to=user.email,
            subject="MissABrick - Verify your email",
            content=f"You can verify your email by clicking on this link {verify_link}",
        )

        return user

    def verify_account(self, token: str, expiration: int = 3600) -> None:
        try:
            email = self.signing_service.urlsafe_loads(token, max_age=expiration)
            user = self.user_dao.get_by_email(email)
            if user is None:
                raise EmailVerificationError(invalid_email=True)

            user.email_verified = True
            user.email_verified_on = dt.datetime.now(tz=dt.UTC)
            self.user_dao.save(user)
        except itsdangerous.SignatureExpired as err:
            raise EmailVerificationError(timeout=True) from err
        except itsdangerous.BadSignature as err:
            raise EmailVerificationError from err
