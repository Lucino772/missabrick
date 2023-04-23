import abc

import sqlalchemy as sa

from app.catalog.models import Minifig
from app.catalog.services._mixins import SqlServiceMixin


class AbstractMinifigsService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self, data: list):
        raise NotImplementedError


class SqlMinifigsService(AbstractMinifigsService, SqlServiceMixin):
    def all(self):
        return self.session.execute(sa.select(Minifig)).scalars().all()

    def get(self, fig_num: str):
        return (
            self.session.execute(
                sa.select(Minifig).filter(Minifig.fig_num == fig_num)
            )
            .scalars()
            .first()
        )

    def imports(self, data: list):
        self.session.execute(sa.delete(Minifig))
        items = map(
            lambda item: Minifig(
                fig_num=item["fig_num"],
                name=item["name"],
                num_parts=int(item["num_parts"]),
                img_url=item["img_url"],
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()
