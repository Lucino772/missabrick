from flask import flash, redirect, render_template, session, url_for

from app.errors import (
    EmailVerificationError,
    InvalidEmailOrPassword,
    PasswordDoesNotMatch,
    UserAlreadyExists,
)
from app.login import blueprint
from app.login.forms import SignInForm, SignUpForm
from app.login.services import user_service


@blueprint.route("/signin", methods=("POST", "GET"))
def signin():
    form = SignInForm()
    if not form.is_submitted():
        return render_template("signin.html", form=form, error=None)

    error = None
    if form.validate():
        try:
            user_service.check_password(form.email.data, form.password.data)
            session["authenticated"] = True
            return redirect(url_for("catalog.index"))
        except InvalidEmailOrPassword:
            error = "The email or password is incorrect"

    return render_template("signin.html", form=form, error=error), 422


@blueprint.route("/signup", methods=("POST", "GET"))
def signup():
    form = SignUpForm()
    if not form.is_submitted():
        return render_template("signup.html", form=form, error=None)

    error = None
    if form.validate():
        try:
            user_service.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                confirm=form.confirm.data,
            )
            session["authenticated"] = True
            return redirect(url_for("catalog.index"))
        except PasswordDoesNotMatch:
            error = "The confirm password does not match the password"
        except UserAlreadyExists:
            error = "This email or username is already used"

    return render_template("signup.html", form=form, error=error), 422


@blueprint.route("/signout", methods=["GET"])
def signout():
    if session.get("authenticated", False) is True:
        session["authenticated"] = False

    return redirect(url_for("catalog.index"))


@blueprint.route("/confirm/<token>")
def verify_email(token: str):
    error = None
    try:
        user_service.verify_email(token)
        flash("Your email was verified", category="info")
        return redirect(url_for("catalog.index"))
    except EmailVerificationError as err:
        if err.invalid_email:
            error = "The email you tried to verify is invalid"
        elif err.timeout:
            error = "The link expired"
        else:
            error = "Could not verify the email address"

    flash(error, category="error")
    return redirect(url_for("catalog.index"))
