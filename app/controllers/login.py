from flask import Blueprint, flash, redirect, render_template, url_for
from flask.views import MethodView
from injector import inject

from app.errors import (
    EmailVerificationError,
    InvalidEmailOrPasswordError,
    PasswordDoesNotMatchError,
    UserAlreadyExistsError,
)
from app.forms.login import SignInForm, SignUpForm
from app.interfaces.services.account import IAccountService
from app.interfaces.services.authentication import IAuthenticationService

blueprint = Blueprint("login", __name__, url_prefix="/auth")


@inject
class SignInView(MethodView):
    def __init__(self, auth_service: "IAuthenticationService") -> None:
        self._auth_service = auth_service
        self._form = SignInForm()

    def get(self):
        return render_template("signin.html", form=self._form, error=None)

    def post(self):
        if not self._form.is_submitted():
            return render_template("signin.html", form=self._form, error=None)

        error = None
        if self._form.validate():
            try:
                self._auth_service.authenticate_with_login(
                    self._form.email.data, self._form.password.data
                )
                return redirect(url_for("explore.index"))
            except InvalidEmailOrPasswordError:
                error = "The email or password is incorrect"

        return render_template("signin.html", form=self._form, error=error)


@inject
class SignUpView(MethodView):
    def __init__(
        self,
        account_service: IAccountService,
        auth_service: IAuthenticationService,
    ) -> None:
        self._account_service = account_service
        self._auth_service = auth_service
        self._form = SignUpForm()

    def get(self):
        return render_template("signup.html", form=self._form, error=None)

    def post(self):
        if not self._form.is_submitted():
            return render_template("signup.html", form=self._form, error=None)

        error = None
        if self._form.validate():
            try:
                user = self._account_service.create_account(
                    username=self._form.username.data,
                    email=self._form.email.data,
                    password=self._form.password.data,
                    confirm=self._form.confirm.data,
                )
                self._auth_service.authenticate_with_login(user.email, user.password)
                return redirect(url_for("explore.index"))
            except PasswordDoesNotMatchError:
                error = "The confirm password does not match the password"
            except UserAlreadyExistsError:
                error = "This email or username is already used"

        return render_template("signup.html", form=self._form, error=error)


@inject
class SignOutView(MethodView):
    def __init__(self, auth_service: IAuthenticationService) -> None:
        self._auth_service = auth_service

    def get(self):
        self._auth_service.deauthenticate()
        return redirect(url_for("explore.index"))


@inject
class VerifyEmailView(MethodView):
    def __init__(self, account_service: IAccountService):
        self._account_service = account_service

    def get(self, token: str):
        error = None
        try:
            self._account_service.verify_account(token)
            flash("Your email was verified", category="info")
            return redirect(url_for("explore.index"))
        except EmailVerificationError as err:
            if err.invalid_email:
                error = "The email you tried to verify is invalid"
            elif err.timeout:
                error = "The link expired"
            else:
                error = "Could not verify the email address"

        flash(error, category="error")
        return redirect(url_for("explore.index"))


blueprint.add_url_rule("/signin", view_func=SignInView.as_view("signin"))
blueprint.add_url_rule("/signup", view_func=SignUpView.as_view("signup"))
blueprint.add_url_rule("/signout", view_func=SignOutView.as_view("signout"))
blueprint.add_url_rule(
    "/confirm/<string:token>",
    view_func=VerifyEmailView.as_view("verify_email"),
)
