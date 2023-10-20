import typing as t

from app.interfaces.services.service import IService


class ISigningService(IService):
    def urlsafe_dumps(self, obj: t.Any) -> t.Union[str, bytes]:
        ...

    def urlsafe_loads(
        self, value: t.Union[str, bytes], max_age: int = None
    ) -> t.Any:
        ...
