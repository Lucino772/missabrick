import abc

import sqlalchemy as sa

from app.catalog.models import PartsRelationship
from app.catalog.services._mixins import SqlServiceMixin


class AbstractPartsRelationshipsService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self, data: list):
        raise NotImplementedError


class SqlPartsRelationshipsService(
    AbstractPartsRelationshipsService, SqlServiceMixin
):
    def all(self):
        return (
            self.session.execute(sa.select(PartsRelationship)).scalars().all()
        )

    def get(self, id: int):
        return (
            self.session.execute(
                sa.select(PartsRelationship).filter(PartsRelationship.id == id)
            )
            .scalars()
            .first()
        )

    def imports(self, data: list):
        self.session.execute(sa.delete(PartsRelationship))
        items = map(
            lambda item: PartsRelationship(
                rel_type=item["rel_type"],
                child_part_id=item["child_part_num"],
                parent_part_id=item["parent_part_num"],
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()
