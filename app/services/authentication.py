import typing as t

from flask import session

from app.errors import InvalidEmailOrPassword
from app.factories import dao_factory
from app.interfaces.factory.service import IServiceFactory
from app.interfaces.services.authentication import IAuthenticationService
from app.models.orm.login import User
from app.services.abstract import AbstractService


class AuthenticationService(AbstractService, IAuthenticationService):
    def __init__(self, factory: IServiceFactory) -> None:
        super().__init__(factory)
        self.user_dao = dao_factory.get_user_dao()

    def authenticate_with_login(self, email: str, password: str) -> None:
        user = self.user_dao.get_by_email(email)
        if user is None or user.password != password:
            raise InvalidEmailOrPassword()

        session["user_id"] = user.id

    def get_current_user(self) -> User:
        user_id = session.get("user_id", None)
        if user_id is None:
            return None

        return self.user_dao.get(user_id)

    def deauthenticate(self) -> None:
        if "user_id" in session:
            session.pop("user_id")
