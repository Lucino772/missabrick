import typing as t

Model_T = t.TypeVar("Model_T")
ModelKey_T = t.TypeVar("ModelKey_T")


class Dao(t.Protocol[Model_T, ModelKey_T]):
    def all(self) -> t.Sequence[Model_T]:  # noqa A003
        ...

    def get(self, ident: ModelKey_T) -> Model_T | None:
        ...

    def save(self, obj: Model_T):
        ...

    def delete(self, obj: Model_T):
        ...
