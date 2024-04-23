from typing import Any, Protocol

from app.interfaces.services.service import IService


class ISigningService(IService, Protocol):
    def urlsafe_dumps(self, obj: Any) -> str | bytes:
        ...

    def urlsafe_loads(self, value: str | bytes, max_age: int | None = None) -> Any:
        ...
