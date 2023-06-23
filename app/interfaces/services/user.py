import typing as t

from app.interfaces.services.service import IService


class IUserService(IService):
    def create_user(
        self, username: str, email: str, password: str, confirm: str
    ):
        ...

    def check_password(self, email: str, password: str):
        ...

    def verify_email(self, token: str, expiration: int = 3600):
        ...
