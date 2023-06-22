import typing as t

from app.interfaces.daos.color import IColorDao
from app.interfaces.daos.element import IElementDao
from app.interfaces.daos.generic_set import IGenericSetDao
from app.interfaces.daos.generic_set_part import IGenericSetPartDao
from app.interfaces.daos.generic_set_rel import IGenericSetRelationshipDao
from app.interfaces.daos.part import IPartDao
from app.interfaces.daos.part_category import IPartCategoryDao
from app.interfaces.daos.theme import IThemeDao
from app.interfaces.daos.year import IYearDao
from app.models.dao.base import BaseDao
from app.models.orm.lego import (
    Color,
    Element,
    GenericSet,
    GenericSetPart,
    GenericSetRelationship,
    Part,
    PartCategory,
    Theme,
    Year,
)


class ColorDao(BaseDao[Color, int], IColorDao):
    ...


class ElementDao(BaseDao[Element, int], IElementDao):
    ...


class GenericSetPartDao(BaseDao[GenericSetPart, int], IGenericSetPartDao):
    ...


class GenericSetRelationshipDao(
    BaseDao[GenericSetRelationship, t.Tuple[str, str]],
    IGenericSetRelationshipDao,
):
    ...


class PartDao(BaseDao[Part, str], IPartDao):
    ...


class PartCategoryDao(BaseDao[PartCategory, int], IPartCategoryDao):
    ...


class ThemeDao(BaseDao[Theme, int], IThemeDao):
    ...


class YearDao(BaseDao[Year, int], IYearDao):
    ...


class GenericSetDao(BaseDao[GenericSet, str], IGenericSetDao):
    def get_subsets(
        self, _set: "GenericSet", quantity: int = 1, recursive: bool = True
    ):
        _subsets: t.List[t.Tuple[GenericSet, int]] = [(_set, quantity)]

        if recursive:
            for subset in _set.children_rel:
                if not subset.child.is_minifig:
                    _subsets.extend(
                        self.get_subsets(
                            subset.child, subset.quantity * quantity, True
                        )
                    )

        return _subsets

    def get_minifigs(
        self, _set: GenericSet, quantity: int = 1, recursive: bool = True
    ):
        _minifigs: t.List[t.Tuple[GenericSet, GenericSet, int]] = []

        for subset, _quantity in self.get_subsets(_set, quantity, recursive):
            for minifig in subset.children_rel:
                if minifig.child.is_minifig:
                    _minifigs.append(
                        (subset, minifig.child, minifig.quantity * _quantity)
                    )

        return _minifigs
