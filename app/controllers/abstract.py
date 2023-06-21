import typing as t
from abc import ABC

from app.interfaces.controllers.controller import IController
from app.interfaces.factory.service import IServiceFactory
from app.interfaces.views.view import IView

View_T = t.TypeVar("View_T", bound=IView)


class AbstractController(ABC, IController, t.Generic[View_T]):
    __slots__ = ("view", "service_factory")

    def __init__(
        self, view: View_T, service_factory: "IServiceFactory"
    ) -> None:
        self.view = view
        self.service_factory = service_factory
