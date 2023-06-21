import os
import typing as t
from abc import ABC, abstractmethod

from flask import abort, make_response, redirect, render_template

from app.factory.controller import ControllerFactory
from app.interfaces.controllers.controller import IController
from app.interfaces.factory.controller import IControllerFactory
from app.interfaces.views.view import IView
from app.types import ControllerFactoryMethod

Controller_T = t.TypeVar("Controller_T", bound=IController)


class AbstractView(ABC, IView, t.Generic[Controller_T]):
    __slots__ = ("controller",)

    controller_factory: ControllerFactoryMethod[Controller_T] = None

    def __init__(self) -> None:
        if not callable(self.controller_factory):
            raise RuntimeError(
                "Failed to get controller, you must set the controller factory method."
            )

        self.controller: Controller_T = self.controller_factory(self)

    def _stream_file_and_remove(self, filename: str, fd: int = None):
        open_path = filename if fd is None else fd

        with open(open_path, "rb", closefd=True) as fp:
            yield from fp

        os.remove(filename)

    def send_file(self, filename: str, source: str, type: str, fd: int = None):
        nbytes = os.stat(source).st_size
        resp = make_response(self._stream_file_and_remove(source, fd))
        resp.headers["Content-Disposition"] = f"inline; filename={filename}"
        resp.headers["Content-Length"] = nbytes
        resp.headers["Content-Type"] = type
        resp.headers["filename"] = filename
        return resp

    def render(self, template: str, **context):
        return render_template(template, **context)

    def abort(self, code: int):
        abort(code)

    def redirect(self, location: str):
        return redirect(location)

    @abstractmethod
    def as_blueprint(self):
        raise NotImplementedError
