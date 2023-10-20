from flask import Blueprint, flash, redirect, render_template, url_for

from app.errors import (
    EmailVerificationError,
    InvalidEmailOrPassword,
    PasswordDoesNotMatch,
    UserAlreadyExists,
)
from app.factories import service_factory
from app.forms.login import SignInForm, SignUpForm

blueprint = Blueprint("login", __name__, url_prefix="/auth")


@blueprint.route("/signin", methods=["POST", "GET"])
def signin():
    form = SignInForm()
    if not form.is_submitted():
        return render_template("signin.html", form=form, error=None)

    error = None
    if form.validate():
        try:
            auth_service = service_factory.get_authentication_service()
            auth_service.authenticate_with_login(
                form.email.data, form.password.data
            )
            return redirect(url_for("explore.index"))
        except InvalidEmailOrPassword:
            error = "The email or password is incorrect"

    return render_template("signin.html", form=form, error=error)


@blueprint.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if not form.is_submitted():
        return render_template("signup.html", form=form, error=None)

    error = None
    if form.validate():
        try:
            account_service = service_factory.get_account_service()
            auth_service = service_factory.get_authentication_service()

            user = account_service.create_account(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                confirm=form.confirm.data,
            )
            auth_service.authenticate_with_login(user.email, user.password)
            return redirect(url_for("explore.index"))
        except PasswordDoesNotMatch:
            error = "The confirm password does not match the password"
        except UserAlreadyExists:
            error = "This email or username is already used"

    return render_template("signup.html", form=form, error=error)


@blueprint.route("/signout", methods=["GET"])
def signout():
    auth_service = service_factory.get_authentication_service()
    auth_service.deauthenticate()
    return redirect(url_for("explore.index"))


@blueprint.route("/confirm/<string:token>")
def verify_email(token: str):
    error = None
    try:
        account_service = service_factory.get_account_service()
        account_service.verify_account(token)
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
