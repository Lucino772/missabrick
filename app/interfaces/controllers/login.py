import typing as t

from app.interfaces.controllers.controller import IController


class ILoginController(IController):
    def signin(self):
        ...

    def signup(self):
        ...

    def signout(self):
        ...

    def verify_email(self, token: str):
        ...
