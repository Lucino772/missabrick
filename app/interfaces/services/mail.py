from typing import Any, Protocol

from app.interfaces.services.service import IService


class IMailService(IService, Protocol):
    def send(self, _from: str, to: str, subject: str, content: str) -> Any: ...
