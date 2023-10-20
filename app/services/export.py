import tempfile
import typing as t

import pandas as pd

from app.errors import SetDoesNotExists
from app.models.orm.lego import GenericSet, GenericSetPart

if t.TYPE_CHECKING:
    from sqlalchemy.orm import scoped_session

    from app.interfaces.daos.generic_set import IGenericSetDao


class ExportService:
    def __init__(
        self,
        *,
        db_session: "scoped_session",
        generic_set_dao: "IGenericSetDao"
    ) -> None:
        self.session = db_session
        self.generic_set_dao = generic_set_dao

    def _format_parts(
        self,
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
                item["fig_num"] = fig_id

            yield item

    def _format_elements(
        self, set_id: str, parts: t.Iterable["GenericSetPart"]
    ):
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

    def export_parts(self, set_id: str, quantity: int = 1):
        parts = []
        fig_parts = []
        elements = []

        _set = self.session.get(GenericSet, set_id)
        if _set is None:
            raise SetDoesNotExists()

        for _subset, _quantity in self.generic_set_dao.get_subsets(
            _set, quantity=quantity, recursive=True
        ):
            parts.extend(
                self._format_parts(_subset.id, _subset.parts, _quantity)
            )
            elements.extend(self._format_elements(_subset.id, _subset.parts))

            for _, minifig, fig_quantity in self.generic_set_dao.get_minifigs(
                _subset, quantity=_quantity, recursive=False
            ):
                fig_parts.extend(
                    self._format_parts(
                        _subset.id, minifig.parts, fig_quantity, minifig.id
                    )
                )
                elements.extend(
                    self._format_elements(_subset.id, minifig.parts)
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

        fd, filename = tempfile.mkstemp()
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            _parts.to_excel(writer, sheet_name="parts", index=False)
            _fig_parts.to_excel(writer, sheet_name="minifigs", index=False)
            _elements.to_excel(writer, sheet_name="elements", index=False)

        return fd, filename
