import typing as t

from app.interfaces.controllers.controller import IController


class IReportController(IController):
    def generate(self):
        ...
