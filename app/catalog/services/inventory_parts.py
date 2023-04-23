import abc

import sqlalchemy as sa

from app.catalog.models import InventoryParts
from app.catalog.services._mixins import SqlServiceMixin


class AbstractInventoryPartsService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self, data: list):
        raise NotImplementedError


class SqlInventoryPartsService(AbstractInventoryPartsService, SqlServiceMixin):
    def all(self):
        return self.session.execute(sa.select(InventoryParts)).scalars().all()

    def get(self, id: int):
        return (
            self.session.execute(
                sa.select(InventoryParts).filter(InventoryParts.id == id)
            )
            .scalars()
            .first()
        )

    def imports(self, data: list):
        self.session.execute(sa.delete(InventoryParts))
        items = map(
            lambda item: InventoryParts(
                inventory_id=int(item["inventory_id"]),
                part_id=item["part_num"],
                color_id=int(item["color_id"]),
                quantity=int(item["quantity"]),
                is_spare=item["is_spare"] == "t",
                img_url=item["img_url"],
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()
