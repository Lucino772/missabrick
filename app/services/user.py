import datetime as dt

import itsdangerous
import sendgrid
from flask import current_app, url_for
from sendgrid.helpers.mail import Content, Email, Mail, To

from app.dao.user import user_dao
from app.errors import (
    EmailVerificationError,
    InvalidEmailOrPassword,
    PasswordDoesNotMatch,
    UserAlreadyExists,
)
from app.models.user import User


def _get_dangerous_serializer():
    return itsdangerous.URLSafeTimedSerializer(
        secret_key=current_app.config["SECRET_KEY"],
        salt=current_app.config["SECURITY_PASSWORD_SALT"],
    )


class UserService:
    def __init__(self, mail_srv: "MailService") -> None:
        self.mail_srv = mail_srv

    def create_user(
        self, username: str, email: str, password: str, confirm: str
    ):
        if password != confirm:
            raise PasswordDoesNotMatch()

        if user_dao.exists(email, username):
            raise UserAlreadyExists()

        user = User(username=username, email=email, password=password)
        user_dao.save(user)

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
        user = user_dao.get_by_email(email)
        if user is None or user.password != password:
            raise InvalidEmailOrPassword()

    def verify_email(self, token: str, expiration: int = 3600):
        try:
            email = _get_dangerous_serializer().loads(
                token, max_age=expiration
            )
            user = user_dao.get_by_email(email)
            if user is None:
                raise EmailVerificationError(invalid_email=True)

            user.email_verified = True
            user.email_verified_on = dt.datetime.now()
            user_dao.save()
        except itsdangerous.SignatureExpired:
            raise EmailVerificationError(timeout=True)
        except itsdangerous.BadSignature:
            raise EmailVerificationError()


class MailService:
    def send(self, _from: str, to: str, subject: str, content: str):
        sg = sendgrid.SendGridAPIClient(
            api_key=current_app.config["SENDGRID_API_KEY"]
        )
        text_content = Content("text/plain", content)
        mail_json = Mail(Email(_from), To(to), subject, text_content).get()
        return sg.send(mail_json)


mail_service = MailService()
user_service = UserService()
