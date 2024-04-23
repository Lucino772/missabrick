from typing import Protocol

from app.interfaces.daos.dao import Dao
from app.models.orm.lego import GenericSet


class IGenericSetDao(Dao[GenericSet, int], Protocol):
    def get_subsets(
        self, _set: GenericSet, quantity: int = ..., *, recursive: bool = ...
    ) -> list[tuple[GenericSet, int]]:
        ...

    def get_minifigs(
        self, _set: GenericSet, quantity: int = ..., *, recursive: bool = ...
    ) -> list[tuple[GenericSet, GenericSet, int]]:
        ...
