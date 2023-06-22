import typing as t

import sqlalchemy as sa

from app.extensions import db
from app.interfaces.daos.dao import Dao

if t.TYPE_CHECKING:
    from sqlalchemy.orm import scoped_session

Model_T = t.TypeVar("Model_T")
ModelKey_T = t.TypeVar("ModelKey_T")


class BaseDao(Dao[Model_T, ModelKey_T]):
    def __init__(self, model: t.Type[Model_T]) -> None:
        self.model = model
        self.session: "scoped_session" = db.session

    def all(self):
        return self.session.execute(sa.select(self.model)).scalars().all()

    def get(self, ident: ModelKey_T):
        return self.session.get(self.model, ident)

    def save(self, obj: Model_T):
        self.session.add(obj)
        self.session.commit()

    def delete(self, obj: Model_T):
        self.session.delete(obj)
        self.session.commit()
