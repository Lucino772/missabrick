from flask import redirect, render_template, session, url_for

from app.login import blueprint
from app.login.forms import SignInForm, SignUpForm
from app.login.utils import (
    ConfirmPasswordDoesNotMatch,
    EmailAlreadyTaken,
    LoginError,
    UsernameAlreadyTaken,
    check_confirm_password,
    check_email,
    check_login,
    check_username,
    create_user,
)


@blueprint.route("/signin", methods=("POST", "GET"))
def signin():
    form = SignInForm()
    if not form.is_submitted():
        return render_template("signin.html", form=form, error=None)

    if form.validate():
        error = None
        try:
            check_login(form.email.data, form.password.data)
        except LoginError:
            error = "The username or password is incorrect"

        if error is not None:
            return render_template("signin.html", form=form, error=error), 422
        else:
            session["authenticated"] = True
            return redirect(url_for("catalog.index"))
    else:
        return render_template("signin.html", form=form, error=None), 422


@blueprint.route("/signup", methods=("POST", "GET"))
def signup():
    form = SignUpForm()
    if not form.is_submitted():
        return render_template("signup.html", form=form, error=None)

    if form.validate():
        error = None
        try:
            check_email(form.email.data)
            check_username(form.username.data)
            check_confirm_password(form.password.data, form.confirm.data)
            create_user(
                form.username.data, form.email.data, form.password.data
            )
        except EmailAlreadyTaken:
            error = "This email address is already used"
        except UsernameAlreadyTaken:
            error = f"The username '{form.username.data}' is not available"
        except ConfirmPasswordDoesNotMatch:
            error = "The confirm password does not match the password"

        if error is not None:
            return render_template("signup.html", form=form, error=error), 422
        else:
            session["authenticated"] = True
            return redirect(url_for("catalog.index"))
    else:
        return render_template("signup.html", form=form, error=None), 422


@blueprint.route("/signout", methods=["GET"])
def signout():
    if session.get("authenticated", False) is True:
        session["authenticated"] = False

    return redirect(url_for("catalog.index"))
