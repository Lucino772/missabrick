from app.controllers.abstract import AbstractController
from app.interfaces.controllers.login import ILoginController
from app.interfaces.views.login import ILoginView


class LoginController(AbstractController[ILoginView], ILoginController):
    def signin(self):
        return super().signin()

    def signup(self):
        return super().signup()

    def signout(self):
        return super().signout()

    def verify_email(self, token: str):
        return super().verify_email(token)
