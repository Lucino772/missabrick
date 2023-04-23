import abc

import sqlalchemy as sa

from app.catalog.models import PartsCategory
from app.catalog.services._mixins import SqlServiceMixin


class AbstractPartsCategoriesService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self, data: list):
        raise NotImplementedError


class SqlPartsCategoriesService(
    AbstractPartsCategoriesService, SqlServiceMixin
):
    def all(self):
        return self.session.execute(sa.select(PartsCategory)).scalars().all()

    def get(self, id: int):
        return (
            self.session.execute(
                sa.select(PartsCategory).filter(PartsCategory.id == id)
            )
            .scalars()
            .first()
        )

    def imports(self, data: list):
        self.session.execute(sa.delete(PartsCategory))
        items = map(
            lambda item: PartsCategory(
                id=int(item["id"]),
                name=item["name"],
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()
