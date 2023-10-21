import typing as t

import sqlalchemy as sa
from injector import inject
from sqlalchemy.orm import scoped_session

Model_T = t.TypeVar("Model_T")
ModelKey_T = t.TypeVar("ModelKey_T")


@inject
class BaseDao(t.Generic[Model_T, ModelKey_T]):
    model: t.ClassVar[t.Type[Model_T]] = None

    def __init__(self, db_session: "scoped_session") -> None:
        self.session = db_session

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
