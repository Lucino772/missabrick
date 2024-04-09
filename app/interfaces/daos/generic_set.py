import typing as t

from app.interfaces.daos.dao import Dao
from app.models.orm.lego import GenericSet


class IGenericSetDao(Dao[GenericSet, int]):
    def get_subsets(
        self, _set: "GenericSet", quantity: int = ..., recursive: bool = ...
    ) -> t.List[t.Tuple["GenericSet", int]]: ...

    def get_minifigs(
        self, _set: "GenericSet", quantity: int = ..., recursive: bool = ...
    ) -> t.List[t.Tuple["GenericSet", "GenericSet", int]]: ...
