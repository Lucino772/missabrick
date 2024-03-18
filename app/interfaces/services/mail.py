import typing as t

from app.interfaces.services.service import IService


class IMailService(IService):
    def send(
        self, _from: str, to: str, subject: str, content: str
    ) -> t.Any: ...
