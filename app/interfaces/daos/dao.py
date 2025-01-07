from collections.abc import Sequence
from typing import Protocol, TypeVar

Model_T = TypeVar("Model_T")
ModelKey_contra = TypeVar("ModelKey_contra", contravariant=True)


class Dao(Protocol[Model_T, ModelKey_contra]):
    def all(self) -> Sequence[Model_T]:  # noqa A003
        ...

    def get(self, ident: ModelKey_contra) -> Model_T | None: ...

    def save(self, obj: Model_T) -> None: ...

    def delete(self, obj: Model_T) -> None: ...
