from typing import Protocol

from app.interfaces.services.service import IService
from app.models.orm.login import User


class IAccountService(IService, Protocol):
    def create_account(
        self, username: str, email: str, password: str, confirm: str
    ) -> User: ...

    def verify_account(self, token: str, expiration: int = ...) -> None: ...
