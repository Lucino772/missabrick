import abc

import sqlalchemy as sa

from app.catalog.models import Element
from app.catalog.services._mixins import SqlServiceMixin


class AbstractElementsService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self, data: list):
        raise NotImplementedError


class SqlElementsService(AbstractElementsService, SqlServiceMixin):
    def all(self):
        return self.session.execute(sa.select(Element)).scalars().all()

    def get(self, id: int):
        return (
            self.session.execute(
                sa.select(Element).filter(Element.element_id == id)
            )
            .scalars()
            .first()
        )

    def imports(self, data: list):
        self.session.execute(sa.delete(Element))
        items = map(
            lambda item: Element(
                element_id=int(item["element_id"]),
                part_id=item["part_num"],
                color_id=int(item["color_id"]),
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()
