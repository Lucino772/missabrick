import abc

import sqlalchemy as sa

from app.catalog.models import InventoryMinifigs
from app.catalog.services._mixins import SqlServiceMixin


class AbstractInventoryMinifigsService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self, data: list):
        raise NotImplementedError


class SqlInventoryMinifigsService(
    AbstractInventoryMinifigsService, SqlServiceMixin
):
    def all(self):
        return (
            self.session.execute(sa.select(InventoryMinifigs)).scalars().all()
        )

    def get(self, id: int):
        return (
            self.session.execute(
                sa.select(InventoryMinifigs).filter(InventoryMinifigs.id == id)
            )
            .scalars()
            .first()
        )

    def imports(self, data: list):
        self.session.execute(sa.delete(InventoryMinifigs))
        items = map(
            lambda item: InventoryMinifigs(
                inventory_id=int(item["inventory_id"]),
                minifig_id=item["fig_num"],
                quantity=int(item["quantity"]),
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()
