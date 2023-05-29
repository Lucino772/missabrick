import abc
import typing as t

import pandas as pd
import sqlalchemy as sa

from app.catalog.models import Inventory, Set, Theme
from app.catalog.services._mixins import SqlServiceMixin


class AbstractSetsService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_parts(
        self,
        set_num: str,
        recursive: bool = True,
        include_minifigs: bool = True,
        include_elements: bool = True,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    def search(
        self,
        search: str,
        paginate: bool = False,
        current_page: int = None,
        page_size: int = None,
        theme: int = None,
        year: str = None,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    def imports(self, data: list):
        raise NotImplementedError

    @abc.abstractmethod
    def get_years(self):
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

    def _get_inventories(
        self, set_num: str, quantity: int = 1, recursive: bool = True
    ):
        aset = (
            self.session.execute(sa.select(Set).filter(Set.set_num == set_num))
            .scalars()
            .first()
        )
        if aset is None:
            return  # TODO: raise exception

        inventory = (
            self.session.execute(
                sa.select(Inventory)
                .filter(Inventory.set_id == aset.set_num)
                .order_by(Inventory.version)
            )
            .scalars()
            .first()
        )
        if inventory is None:
            return  # TODO: raise exception

        inventories = [(inventory, quantity)]

        if recursive is True:
            for inv_set in inventory.inventory_sets:
                inventories += self._get_inventories(
                    inv_set.set_id, inv_set.quantity * quantity, recursive=True
                )

        return inventories

    def _format_elements(self, _list):
        for _tuple in _list:
            if len(_tuple) == 3:
                set_num, inv_parts, qty = _tuple
                fig_num = None
            else:
                set_num, fig_num, inv_parts, qty = _tuple

            for inv_part in inv_parts:
                results = (
                    self.session.execute(
                        inv_part.part.elements.filter_by(color=inv_part.color)
                    )
                    .scalars()
                    .all()
                )

                if len(results) == 0:
                    yield {
                        "set_num": set_num,
                        "part_num": inv_part.part.part_num,
                        "color_id": inv_part.color.id,
                        "element_id": None,
                    }
                else:
                    for elem in results:
                        yield {
                            "set_num": set_num,
                            "part_num": inv_part.part.part_num,
                            "color_id": inv_part.color.id,
                            "element_id": elem.element_id,
                        }

    def _format_parts(self, _list):
        for _tuple in _list:
            if len(_tuple) == 3:
                set_num, inv_parts, qty = _tuple
                fig_num = None
            else:
                set_num, fig_num, inv_parts, qty = _tuple

            for inv_part in inv_parts:
                item = {
                    "set_num": set_num,
                    "part_num": inv_part.part.part_num,
                    "part_name": inv_part.part.name,
                    "part_material": inv_part.part.part_material,
                    "color_id": inv_part.color.id,
                    "color_name": inv_part.color.name,
                    "color_rgb": inv_part.color.rgb,
                    "color_is_trans": inv_part.color.is_trans,
                    "is_spare": inv_part.is_spare,
                    "img_url": inv_part.img_url,
                    "quantity": inv_part.quantity * qty,
                }
                if fig_num is not None:
                    item["fig_num"] = fig_num

                yield item

    def get_parts(
        self,
        set_num: str,
        quantity: int = 1,
        recursive: bool = True,
        include_minifigs: bool = True,
        include_elements: bool = True,
    ):
        invs = self._get_inventories(set_num, quantity, recursive)

        parts = []
        fig_parts = []
        for inv_set, _quantity in invs:
            parts.append(
                (inv_set._set.set_num, inv_set.inventory_parts, _quantity)
            )

            if include_minifigs:
                for inv_fig in inv_set.inventory_minifigs:
                    inv_fig_parts = (
                        self.session.execute(
                            inv_fig.minifig.inventories.order_by(
                                Inventory.version
                            )
                        )
                        .scalars()
                        .first()
                        .inventory_parts
                    )

                    fig_parts.append(
                        (
                            inv_set._set.set_num,
                            inv_fig.minifig.fig_num,
                            inv_fig_parts,
                            _quantity * inv_fig.quantity,
                        )
                    )

        elements_parts = []
        if include_elements:
            elements_parts = parts + fig_parts

        _parts = pd.DataFrame(
            self._format_parts(parts),
            columns=[
                "set_num",
                "part_num",
                "part_name",
                "part_material",
                "color_id",
                "color_name",
                "color_rgb",
                "color_is_trans",
                "is_spare",
                "img_url",
                "quantity",
            ],
        )
        _fig_parts = pd.DataFrame(
            self._format_parts(fig_parts),
            columns=[
                "set_num",
                "fig_num",
                "part_num",
                "part_name",
                "part_material",
                "color_id",
                "color_name",
                "color_rgb",
                "color_is_trans",
                "is_spare",
                "img_url",
                "quantity",
            ],
        )
        _elements = pd.DataFrame(
            self._format_elements(elements_parts),
            columns=["set_num", "part_num", "color_id", "element_id"],
        )

        return _parts, _fig_parts, _elements

    def search(
        self,
        search: str,
        paginate: bool = False,
        current_page: int = None,
        page_size: int = None,
        theme: int = None,
        year: int = None,
    ):
        select = (
            sa.select(Set)
            .filter(Set.set_num.contains(search))
            .order_by(Set.year)
        )

        if theme is not None:
            select = select.filter(Set.theme_id == theme)
        if year is not None:
            select = select.filter(Set.year == year)

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

    def get_years(self):
        return (
            self.session.execute(
                sa.select(Set.year).distinct().order_by(Set.year)
            )
            .scalars()
            .all()
        )
