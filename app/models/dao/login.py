import sqlalchemy as sa
from injector import inject

from app.models.dao.base import BaseDao
from app.models.orm.login import User

_sentinel = object()


@inject
class UserDao(BaseDao[User, int]):
    model = User

    def exists(self, email: str = _sentinel, username: str = _sentinel) -> bool:
        conditions = []
        if email is not _sentinel:
            conditions.append(User.email == email)
        if username is not _sentinel:
            conditions.append(User.username == username)

        if len(conditions) == 0:
            return False

        query = sa.select(User).where(sa.or_(*conditions))
        return self.session.execute(query).scalars().first() is not None

    def get_by_email(self, email: str) -> User | None:
        return self.session.execute(
            sa.select(User).filter(User.email == email)
        ).scalar_one_or_none()
