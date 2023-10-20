import typing as t

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


class ColorDao(BaseDao[Color, int]):
    model = Color


class ElementDao(BaseDao[Element, int]):
    model = Element


class GenericSetPartDao(BaseDao[GenericSetPart, int]):
    model = GenericSetPart


class GenericSetRelationshipDao(
    BaseDao[GenericSetRelationship, t.Tuple[str, str]]
):
    model = GenericSetRelationship


class PartDao(BaseDao[Part, str]):
    model = Part


class PartCategoryDao(BaseDao[PartCategory, int]):
    model = PartCategory


class ThemeDao(BaseDao[Theme, int]):
    model = Theme


class YearDao(BaseDao[Year, int]):
    model = Year


class GenericSetDao(BaseDao[GenericSet, str]):
    model = GenericSet

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
