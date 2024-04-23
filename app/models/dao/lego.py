from injector import inject

from app.models.dao.base import BaseDao
from app.models.orm.lego import GenericSet, Theme, Year


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
        self, _set: "GenericSet", quantity: int = 1, *, recursive: bool = True
    ):
        _subsets: list[tuple[GenericSet, int]] = [(_set, quantity)]

        if recursive:
            for subset in _set.children_rel:
                if not subset.child.is_minifig:
                    _subsets.extend(
                        self.get_subsets(
                            subset.child, subset.quantity * quantity, recursive=True
                        )
                    )

        return _subsets

    def get_minifigs(
        self, _set: GenericSet, quantity: int = 1, *, recursive: bool = True
    ):
        _minifigs: list[tuple[GenericSet, GenericSet, int]] = [
            (subset, minifig.child, minifig.quantity * _quantity)
            for subset, _quantity in self.get_subsets(
                _set, quantity, recursive=recursive
            )
            for minifig in subset.children_rel
            if minifig.child.is_minifig
        ]
        return _minifigs
