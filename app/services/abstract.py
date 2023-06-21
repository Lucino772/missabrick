from abc import ABC

from app.interfaces.factory.service import IServiceFactory
from app.interfaces.services.service import IService


class AbstractService(ABC, IService):
    __slots__ = ("service_factory",)

    def __init__(self, factory: "IServiceFactory") -> None:
        self.service_factory = factory
