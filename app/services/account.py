import datetime as dt

import itsdangerous
from flask import url_for

from app.errors import (
    EmailVerificationError,
    PasswordDoesNotMatch,
    UserAlreadyExists,
)
from app.factories import dao_factory, service_factory
from app.models.orm.login import User


class AccountService:
    def __init__(self) -> None:
        self.user_dao = dao_factory.get_user_dao()
        self.signing_service = service_factory.get_signing_service()
        self.mail_service = service_factory.get_mail_service()

    def create_account(
        self, username: str, email: str, password: str, confirm: str
    ) -> User:
        if password != confirm:
            raise PasswordDoesNotMatch()

        if self.user_dao.exists(email, username):
            raise UserAlreadyExists()

        user = User(username=username, email=email, password=password)
        self.user_dao.save(user)

        # Send email confirmation link
        token = self.signing_service.urlsafe_dumps(user.email)
        verify_link = url_for(
            "login.verify_email", token=token, _external=True
        )
        self.mail_service.send(
            _from="noreply-missabrick@lucapalmi.com",
            to=user.email,
            subject="MissABrick - Verify your email",
            content=f"You can verify your email by clicking on this link: {verify_link}",
        )

        return user

    def verify_account(self, token: str, expiration: int = 3600) -> None:
        try:
            email = self.signing_service.urlsafe_loads(
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
