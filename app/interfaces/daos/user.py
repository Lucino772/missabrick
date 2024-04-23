from typing import Protocol

from app.interfaces.daos.dao import Dao
from app.models.orm.login import User


class IUserDao(Dao[User, int], Protocol):
    def exists(self, email: str = ..., username: str = ...) -> bool:
        ...

    def get_by_email(self, email: str) -> User | None:
        ...
