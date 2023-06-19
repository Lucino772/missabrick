import typing as t
from abc import ABC, abstractmethod

from flask import render_template

from app.factory.controller import ControllerFactory
from app.interfaces.controllers.controller import IController
from app.interfaces.factory.controller import IControllerFactory
from app.interfaces.views.view import IView

Controller_T = t.TypeVar("Controller_T", bound=IController)


class AbstractView(ABC, IView, t.Generic[Controller_T]):
    __slots__ = ("controller", "controller_factory")

    controller_factory: IControllerFactory = ControllerFactory()

    def __init__(self) -> None:
        self.controller: Controller_T = self.controller_factory.get_controller(
            self
        )

    def render(self, template: str, **context):
        return render_template(template, **context)

    @abstractmethod
    def as_blueprint(self):
        raise NotImplementedError
