import json
import re
import typing as t

import pandas as pd
import sqlalchemy as sa

from app.catalog.models import GenericSet, GenericSetPart, Theme, Year
from app.errors import SetDoesNotExists
from app.extensions import db

if t.TYPE_CHECKING:
    from sqlalchemy.orm import Session


class CatalogService:
    __slots__ = ("db", "session")

    def __init__(self) -> None:
        self.db = db
        self.session: "Session" = db.session

    @staticmethod
    def _parse_search_query(search: str):
        keyword_regex = r'(\w+):(("(.*?)")|(\w+))'
        groups = re.findall(keyword_regex, search)
        keywords = [(group[0], group[3] or group[4]) for group in groups]
        return keywords, re.sub(
            r" +", " ", re.sub(keyword_regex, "", search).strip()
        )

    def search_sets(
        self,
        query: str,
        paginate: bool = False,
        current_page: int = None,
        page_size: int = None,
    ):
        keywords, search = self._parse_search_query(query)

        select = (
            sa.select(GenericSet)
            .filter(GenericSet.is_minifig.is_(False))
            .join(Year, GenericSet.year_id == Year.id)
            .order_by(Year.name)
        )
        if len(search) > 0:
            select = select.filter(
                sa.or_(
                    GenericSet.id.contains(search),
                    GenericSet.name.contains(search),
                )
            )

        for key, value in keywords:
            if key == "theme":
                theme_ids = (
                    self.session.execute(
                        sa.select(Theme.id).filter(
                            Theme.name.contains(str(value))
                        )
                    )
                    .scalars()
                    .all()
                )
                if len(theme_ids) > 0:
                    select = select.filter(GenericSet.theme_id.in_(theme_ids))
            elif key == "year" and str(value).isnumeric():
                year_ids = (
                    self.session.execute(
                        sa.select(Year.id).filter(Year.name == int(value))
                    )
                    .scalars()
                    .all()
                )
                if len(year_ids) > 0:
                    select = select.filter(GenericSet.year_id.in_(year_ids))
            elif key == "name":
                select = select.filter(GenericSet.name.contains(str(value)))
            elif key == "id":
                select = select.filter(GenericSet.id.contains(str(value)))

        if paginate:
            return self.db.paginate(
                select, page=current_page, per_page=page_size
            )
        else:
            return self.session.execute(select).scalars().all()

    def get_years(self):
        return self.session.execute(sa.select(Year.name)).scalars().all()

    def get_themes(self):
        return self.session.execute(sa.select(Theme.name)).scalars().all()

    def _get_subsets(self, set_id: int, quantity: int):
        _set = (
            self.session.execute(
                sa.select(GenericSet).filter(GenericSet.id == set_id)
            )
            .scalars()
            .first()
        )

        if _set is None:
            raise SetDoesNotExists()

        _subsets = [(_set, quantity)]
        for subset in _set.children_rel:
            if not subset.child.is_minifig:
                _subsets.extend(
                    self._get_subsets(
                        subset.child_id, subset.quantity * quantity
                    )
                )

        return _subsets

    @staticmethod
    def _format_parts(
        set_id: str,
        parts: t.Iterable["GenericSetPart"],
        quantity: int = 1,
        fig_id: str = None,
    ):
        for set_part in parts:
            item = {
                "set_num": set_id,
                "part_num": set_part.part.id,
                "part_name": set_part.part.name,
                "part_material": set_part.part.material,
                "color_id": set_part.color.id,
                "color_name": set_part.color.name,
                "color_rgb": set_part.color.rgb,
                "color_is_trans": set_part.color.is_trans,
                "is_spare": set_part.is_spare,
                "img_url": set_part.img_url,
                "quantity": set_part.quantity * quantity,
            }
            if fig_id is not None:
                item["fig_id"] = fig_id

            yield item

    @staticmethod
    def _format_elements(set_id: str, parts: t.Iterable["GenericSetPart"]):
        for set_part in parts:
            related_elements = list(set_part.get_related_elements())
            if len(related_elements) > 0:
                for element in set_part.get_related_elements():
                    yield {
                        "set_num": set_id,
                        "part_num": set_part.part_id,
                        "color_id": set_part.color_id,
                        "element_id": element.id,
                    }
            else:
                yield {
                    "set_num": set_id,
                    "part_num": set_part.part_id,
                    "color_id": set_part.color_id,
                    "element_id": None,
                }

    def get_parts(
        self,
        set_id: str,
        quantity: int = 1,
    ):
        parts = []
        fig_parts = []
        elements = []

        for _subset, _quantity in self._get_subsets(set_id, quantity):
            parts.extend(
                self._format_parts(_subset.id, _subset.parts, _quantity)
            )
            elements.extend(self._format_elements(_subset.id, _subset.parts))

            for minifig_rel in _subset.children_rel:
                if minifig_rel.child.is_minifig:
                    fig_parts.extend(
                        self._format_parts(
                            _subset.id,
                            minifig_rel.child.parts,
                            minifig_rel.quantity * _quantity,
                            minifig_rel.child.id,
                        )
                    )
                    elements.extend(
                        self._format_elements(
                            _subset.id,
                            minifig_rel.child.parts,
                        )
                    )

        _parts = pd.DataFrame(
            parts,
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
            fig_parts,
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
            elements,
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
