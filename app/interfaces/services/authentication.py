from typing import Protocol

from app.interfaces.services.service import IService
from app.models.orm.login import User


class IAuthenticationService(IService, Protocol):
    def authenticate_with_login(self, email: str, password: str) -> None:
        ...

    def get_current_user(self) -> User | None:
        ...

    def deauthenticate(self) -> None:
        ...
