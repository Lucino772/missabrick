import abc

import sqlalchemy as sa

from app.catalog.models import InventorySets
from app.catalog.services._mixins import SqlServiceMixin


class AbstractInventorySetsService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self, data: list):
        raise NotImplementedError


class SqlInventorySetsService(AbstractInventorySetsService, SqlServiceMixin):
    def all(self):
        return self.session.execute(sa.select(InventorySets)).scalars().all()

    def get(self, id: int):
        return (
            self.session.execute(
                sa.select(InventorySets).filter(InventorySets.id == id)
            )
            .scalars()
            .first()
        )

    def imports(self, data: list):
        self.session.execute(sa.delete(InventorySets))
        items = map(
            lambda item: InventorySets(
                inventory_id=int(item["inventory_id"]),
                set_id=item["set_num"],
                quantity=int(item["quantity"]),
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()
