import os
import typing as t
from abc import ABC, abstractmethod

from flask import make_response, render_template

from app.factory.controller import ControllerFactory
from app.interfaces.controllers.controller import IController
from app.interfaces.factory.controller import IControllerFactory
from app.interfaces.views.view import IView

Controller_T = t.TypeVar("Controller_T", bound=IController)


class AbstractView(ABC, IView, t.Generic[Controller_T]):
    __slots__ = ("controller",)

    controller_factory: IControllerFactory = ControllerFactory()

    def __init__(self) -> None:
        self.controller: Controller_T = self.controller_factory.get_controller(
            self
        )

    def _stream_file_and_remove(filename: str, fd: int = None):
        open_path = filename if fd is None else fd

        with open(open_path, "rb", closefd=True) as fp:
            yield from fp

        os.remove(filename)

    def send_file(self, filename: str, source: str, type: str, fd: int = None):
        nbytes = os.stat(source).st_size
        return make_response(
            self._stream_file_and_remove(source, fd),
            headers={
                "Content-Disposition": f"inline; filename={filename}",
                "Content-Length": nbytes,
                "Content-Type": type,
                "filename": filename,
            },
        )

    def render(self, template: str, **context):
        return render_template(template, **context)

    @abstractmethod
    def as_blueprint(self):
        raise NotImplementedError
