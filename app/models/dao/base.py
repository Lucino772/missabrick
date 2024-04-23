from collections.abc import Sequence
from typing import Generic, TypeVar

import sqlalchemy as sa
from injector import inject
from sqlalchemy.orm import scoped_session

Model_T = TypeVar("Model_T")
ModelKey_T = TypeVar("ModelKey_T")


@inject
class BaseDao(Generic[Model_T, ModelKey_T]):
    model: type[Model_T]

    def __init__(self, db_session: scoped_session) -> None:
        self.session = db_session

    def __init_subclass__(cls, model: type[Model_T]) -> None:
        cls.model = model

    def all(self) -> Sequence[Model_T]:  # noqa A003
        return self.session.execute(sa.select(self.model)).scalars().all()

    def get(self, ident: ModelKey_T) -> Model_T | None:
        return self.session.get(self.model, ident)

    def save(self, obj: Model_T) -> None:
        self.session.add(obj)
        self.session.commit()

    def delete(self, obj: Model_T) -> None:
        self.session.delete(obj)
        self.session.commit()
