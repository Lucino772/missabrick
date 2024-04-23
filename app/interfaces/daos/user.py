from app.interfaces.daos.dao import Dao
from app.models.orm.login import User


class IUserDao(Dao[User, int]):
    def exists(self, email: str = ..., username: str = ...) -> bool:
        ...

    def get_by_email(self, email: str) -> User | None:
        ...
