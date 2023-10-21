import typing as t

from injector import inject

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


@inject
class ColorDao(BaseDao[Color, int]):
    model = Color


@inject
class ElementDao(BaseDao[Element, int]):
    model = Element


@inject
class GenericSetPartDao(BaseDao[GenericSetPart, int]):
    model = GenericSetPart


@inject
class GenericSetRelationshipDao(
    BaseDao[GenericSetRelationship, t.Tuple[str, str]]
):
    model = GenericSetRelationship


@inject
class PartDao(BaseDao[Part, str]):
    model = Part


@inject
class PartCategoryDao(BaseDao[PartCategory, int]):
    model = PartCategory


@inject
class ThemeDao(BaseDao[Theme, int]):
    model = Theme


@inject
class YearDao(BaseDao[Year, int]):
    model = Year


@inject
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
