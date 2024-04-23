import typing as t

from app.interfaces.services.service import IService


class ISigningService(IService):
    def urlsafe_dumps(self, obj: t.Any) -> str | bytes:
        ...

    def urlsafe_loads(self, value: str | bytes, max_age: int | None = None) -> t.Any:
        ...
