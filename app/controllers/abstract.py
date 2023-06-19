import typing as t
from abc import ABC

from app.interfaces.controllers.controller import IController
from app.interfaces.views.view import IView

View_T = t.TypeVar("View_T", bound=IView)


class AbstractController(ABC, IController, t.Generic[View_T]):
    __slots__ = ("view",)

    def __init__(self, view: View_T) -> None:
        self.view = view
