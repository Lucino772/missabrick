import abc

import sqlalchemy as sa

from app.catalog.models import Theme
from app.catalog.services._mixins import SqlServiceMixin


class AbstractThemesService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self, data: list):
        raise NotImplementedError


class SqlThemesService(AbstractThemesService, SqlServiceMixin):
    def all(self):
        return self.session.execute(sa.select(Theme)).scalars().all()

    def get(self, id: int):
        return (
            self.session.execute(sa.select(Theme).filter(Theme.id == id))
            .scalars()
            .first()
        )

    def imports(self, data: list):
        self.session.execute(sa.delete(Theme))

        def _to_model(item: dict):
            if item["parent_id"].isnumeric():
                parent_id = int(item["parent_id"])
            else:
                parent_id = None

            return Theme(
                id=int(item["id"]),
                name=item["name"],
                parent_id=parent_id,
            )

        items = map(_to_model, data)
        self.session.add_all(items)
        self.session.commit()
