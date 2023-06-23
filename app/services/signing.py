import typing as t

import itsdangerous

from app.interfaces.factory.service import IServiceFactory
from app.interfaces.services.signing import ISigningService
from app.services.abstract import AbstractService


class SigningService(AbstractService, ISigningService):
    def __init__(
        self,
        factory: IServiceFactory,
        secret_key: t.Union[str, bytes],
        salt: t.Union[str, bytes],
    ) -> None:
        super().__init__(factory)
        self._secret_key = secret_key
        self._salt = salt

    def _get_urlsafe_serializer(self):
        return itsdangerous.URLSafeTimedSerializer(
            secret_key=self._secret_key,
            salt=self._salt,
        )

    def urlsafe_dumps(self, obj: t.Any) -> str:
        serializer = self._get_urlsafe_serializer()
        return serializer.dumps(obj)

    def urlsafe_loads(self, value: str, max_age: int = None) -> t.Any:
        serializer = self._get_urlsafe_serializer()
        return serializer.loads(value, max_age=max_age)
