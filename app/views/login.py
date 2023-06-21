from flask import Blueprint

from app.factories import controller_factory
from app.interfaces.controllers.login import ILoginController
from app.interfaces.views.login import ILoginView
from app.views.abstract import AbstractView


class LoginView(AbstractView[ILoginController], ILoginView):
    controller_factory = controller_factory.get_login_controller

    def signin(self):
        return self.controller.signin()

    def signup(self):
        return self.controller.signup()

    def signout(self):
        return self.controller.signout()

    def verify_mail(self, token: str):
        return self.controller.verify_email(token)

    def as_blueprint(self):
        login_bp = Blueprint("login", __name__, url_prefix="/auth")
        login_bp.add_url_rule(
            "/signin", view_func=self.signin, methods=["POST", "GET"]
        )
        login_bp.add_url_rule(
            "/signup", view_func=self.signup, methods=["POST", "GET"]
        )
        login_bp.add_url_rule(
            "/signout", view_func=self.signout, methods=["GET"]
        )
        login_bp.add_url_rule("/confirm/<token>", view_func=self.verify_mail)
        return login_bp
