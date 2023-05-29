import sqlalchemy as sa

from app.dao._generic import GenericDao
from app.models.user import User

MISSING = type("Missing", tuple(), {})()


class UserDao(GenericDao[User]):
    def __init__(self) -> None:
        super().__init__(User)

    def exists(self, email: str = MISSING, username: str = MISSING):
        conditions = []
        if email is not MISSING:
            conditions.append(User.email == email)
        if username is not MISSING:
            conditions.append(User.username == username)

        if len(conditions) == 0:
            return False

        query = sa.select(User).where(sa.or_(*conditions))
        return self.session.execute(query).scalars().first() is not None

    def get_by_email(self, email: str):
        return self.session.execute(
            sa.select(User).filter(User.email == email)
        ).scalar_one_or_none()


user_dao = UserDao()
