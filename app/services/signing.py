import typing as t

import itsdangerous
from flask import Config
from injector import inject


@inject
class SigningService:
    def __init__(self, config: Config) -> None:
        self._secret_key = config["SECRET_KEY"]
        self._salt = config["SECURITY_PASSWORD_SALT"]

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
