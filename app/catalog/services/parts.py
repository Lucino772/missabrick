import abc

import sqlalchemy as sa

from app.catalog.models import Part
from app.catalog.services._mixins import SqlServiceMixin


class AbstractPartsService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self, data: list):
        raise NotImplementedError


class SqlPartsService(AbstractPartsService, SqlServiceMixin):
    def all(self):
        return self.session.execute(sa.select(Part)).scalars().all()

    def get(self, part_num: str):
        return (
            self.session.execute(
                sa.select(Part).filter(Part.part_num == part_num)
            )
            .scalars()
            .first()
        )

    def imports(self, data: list):
        self.session.execute(sa.delete(Part))
        items = map(
            lambda item: Part(
                part_num=item["part_num"],
                name=item["name"],
                part_material=item["part_material"],
                part_category_id=int(item["part_cat_id"]),
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()
