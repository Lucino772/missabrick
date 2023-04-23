import abc

import sqlalchemy as sa

from app.catalog.models import Color
from app.catalog.services._mixins import SqlServiceMixin


class AbstractColorsService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self, data: list):
        raise NotImplementedError


class SqlColorsService(AbstractColorsService, SqlServiceMixin):
    def all(self):
        return self.session.execute(sa.select(Color)).scalars().all()

    def get(self, id: int):
        return (
            self.session.execute(sa.select(Color).filter(Color.id == id))
            .scalars()
            .first()
        )

    def imports(self, data: list):
        self.session.execute(sa.delete(Color))
        items = map(
            lambda item: Color(
                id=int(item["id"]),
                name=item["name"],
                rgb=item["rgb"],
                is_trans=(item["is_trans"] == "t"),
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()
