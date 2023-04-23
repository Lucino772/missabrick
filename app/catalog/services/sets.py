import abc
import typing as t

import sqlalchemy as sa

from app.catalog.models import Set
from app.catalog.services._mixins import SqlServiceMixin


class AbstractSetsService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: str):
        raise NotImplementedError

    @abc.abstractmethod
    def search(
        self,
        search: str,
        paginate: bool = False,
        current_page: int = None,
        page_size: int = None,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self, data: list):
        raise NotImplementedError


class SqlSetsService(AbstractSetsService, SqlServiceMixin):
    def all(self):
        return self.session.execute(sa.select(Set)).scalars().all()

    def get(self, set_num: str):
        return (
            self.session.execute(sa.select(Set).filter(Set.set_num == set_num))
            .scalars()
            .first()
        )

    def search(
        self,
        search: str,
        paginate: bool = False,
        current_page: int = None,
        page_size: int = None,
    ):
        select = (
            sa.select(Set)
            .filter(Set.set_num.contains(search))
            .order_by(Set.year)
        )
        if paginate:
            return self.db.paginate(
                select, page=current_page, per_page=page_size
            )
        else:
            return self.session.execute(select).scalars().all()

    def imports(self, data: t.Iterable[dict]):
        self.session.execute(sa.delete(Set))
        items = map(
            lambda item: Set(
                set_num=item["set_num"],
                name=item["name"],
                year=int(item["year"]),
                theme_id=int(item["theme_id"]),
                num_parts=int(item["num_parts"]),
                img_url=item["img_url"],
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()
