import json
import re
import typing as t

import pandas as pd

from app.dao.catalog import (
    inv_minifig_dao,
    inv_part_dao,
    inventory_dao,
    set_dao,
    theme_dao,
)
from app.extensions import db


def _parse_search_query(search: str):
    keyword_regex = r'(\w+):(("(.*?)")|(\w+))'
    groups = re.findall(keyword_regex, search)
    keywords = [(group[0], group[3] or group[4]) for group in groups]
    return keywords, re.sub(
        r" +", " ", re.sub(keyword_regex, "", search).strip()
    )


class CatalogService:
    def _format_elements(self, _list):
        for _tuple in _list:
            if len(_tuple) == 3:
                set_num, inv_parts, qty = _tuple
                fig_num = None
            else:
                set_num, fig_num, inv_parts, qty = _tuple

            for inv_part in inv_parts:
                for value in inv_part_dao.format_elements(inv_part):
                    yield {**value, "set_num": set_num}

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

    def search_sets(
        self,
        search: str,
        paginate: bool = False,
        current_page: int = None,
        page_size: int = None,
    ):
        keywords, ft_search = _parse_search_query(search)
        return set_dao.search(
            keywords, ft_search, paginate, current_page, page_size
        )

    def get_years(self):
        return set_dao.get_years()

    def get_themes(self):
        return list({theme.name for theme in theme_dao.all()})

    def get_parts(
        self,
        set_id: str,
        quantity: int = 1,
        include_minifigs: bool = True,
        include_elements: bool = True,
    ):
        inventories = inventory_dao.get_inventories(
            set_id, quantity, recursive=True
        )

        parts = []
        fig_parts = []
        for inv_set, _quantity in inventories:
            parts.append(
                (inv_set._set.set_num, inv_set.inventory_parts, _quantity)
            )

            if include_minifigs:
                for inv_fig in inv_set.inventory_minifigs:
                    fig_parts.append(
                        (
                            inv_set._set.set_num,
                            inv_fig.minifig.fig_num,
                            inv_minifig_dao.get_parts(inv_fig),
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


class ReportService:
    @staticmethod
    def _find_first_key(
        possible_values: t.Iterable[str], search_list: t.Iterable[str]
    ):
        for key in possible_values:
            if key in search_list:
                return key

    def generate_report(
        self,
        parts: pd.DataFrame,
        fig_parts: pd.DataFrame,
        elements: pd.DataFrame,
    ):
        count_keys = ["count", "current"]
        parts_count_key = self._find_first_key(count_keys, parts.columns)
        fig_parts_count_key = self._find_first_key(
            count_keys, fig_parts.columns
        )

        if parts_count_key is None:
            parts["count"] = 0
            parts_count_key = "count"

        if fig_parts_count_key is None:
            fig_parts["count"] = 0
            fig_parts_count_key = "count"

        # Calculate missing pieces
        parts["missing"] = parts["quantity"] - parts[parts_count_key]
        fig_parts["missing"] = (
            fig_parts["quantity"] - fig_parts[fig_parts_count_key]
        )

        parts_data = json.loads(parts.to_json(orient="table")).get("data", [])
        fig_parts_data = json.loads(fig_parts.to_json(orient="table")).get(
            "data", []
        )

        return {"parts": parts_data, "fig_parts": fig_parts_data}


catalog_service = CatalogService()
report_service = ReportService()
