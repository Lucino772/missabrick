from flask import flash, redirect, render_template, session, url_for

from app.login import blueprint
from app.login.forms import SignInForm, SignUpForm
from app.login.utils import (
    ConfirmPasswordDoesNotMatch,
    EmailAlreadyTaken,
    EmailVerificationError,
    LoginError,
    UsernameAlreadyTaken,
    check_confirm_password,
    check_email,
    check_login,
    check_username,
    confirm_verify_mail_token,
    create_user,
    generate_verify_mail_token,
    send_verify_mail,
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
            # Send Email verification mail
            token = generate_verify_mail_token(form.email.data)
            verify_url = url_for(
                "login.verify_email", token=token, _external=True
            )
            send_verify_mail(form.email.data, verify_url)
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


@blueprint.route("/confirm/<token>")
def verify_email(token: str):
    try:
        confirm_verify_mail_token(token)
        flash("Your email was verified", category="info")
        return redirect(url_for("catalog.index"))
    except EmailVerificationError as err:
        if err.invalid_email:
            flash("The email you tried to verify is invalid", category="error")
        elif err.timeout:
            flash("The link expired", category="error")
        else:
            flash("Could not verify the email address", category="error")

        return redirect(url_for("catalog.index"))
