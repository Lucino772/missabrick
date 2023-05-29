import typing as t

import sqlalchemy as sa
from sqlalchemy.orm import Session

from app.extensions import db

MISSING = type("Missing", tuple(), {})()

T = t.TypeVar("T")


class GenericDao(t.Generic[T]):
    def __init__(self, model: t.Type[T]) -> None:
        self.model = model
        self.session: Session = db.session

    def all(self):
        return self.session.execute(sa.select(self.model)).scalars().all()

    def get(self, id: int):
        return self.session.get(self.model, id)

    def save(self, user: T):
        self.session.add(user)
        self.session.commit()

    def delete(self, user: T):
        self.session.delete(user)
        self.session.commit()
