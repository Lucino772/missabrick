import abc

import sqlalchemy as sa

from app.catalog.models import Inventory
from app.catalog.services._mixins import SqlServiceMixin


class AbstractInventoriesService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self, data: list):
        raise NotImplementedError


class SqlInventoriesService(AbstractInventoriesService, SqlServiceMixin):
    def all(self):
        return self.session.execute(sa.select(Inventory)).scalars().all()

    def get(self, id: int):
        return (
            self.session.execute(
                sa.select(Inventory).filter(Inventory.id == id)
            )
            .scalars()
            .first()
        )

    def imports(self, data: list):
        self.session.execute(sa.delete(Inventory))

        def _to_model(item: dict):
            is_minifig = item["set_num"].startswith("fig-")
            if is_minifig:
                set_id = None
                minifig_id = item["set_num"]
            else:
                set_id = item["set_num"]
                minifig_id = None

            return Inventory(
                id=int(item["id"]),
                version=int(item["version"]),
                is_minifig=is_minifig,
                set_id=set_id,
                minifig_id=minifig_id,
            )

        items = map(_to_model, data)
        self.session.add_all(items)
        self.session.commit()
