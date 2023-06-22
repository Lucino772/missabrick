import typing as t

Model_T = t.TypeVar("Model_T")
ModelKey_T = t.TypeVar("ModelKey_T")


class Dao(t.Protocol[Model_T, ModelKey_T]):
    def all(self) -> t.Sequence[Model_T]:
        ...

    def get(self, ident: ModelKey_T) -> t.Optional[Model_T]:
        ...

    def save(self, obj: Model_T):
        ...

    def delete(self, obj: Model_T):
        ...
