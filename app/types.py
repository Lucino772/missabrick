import typing as t

from app.interfaces.controllers.controller import IController
from app.interfaces.views.view import IView

Controller_T = t.TypeVar("Controller_T", bound=IController)
ControllerFactoryMethod = t.Callable[[IView], Controller_T]
