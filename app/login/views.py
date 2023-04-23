from flask import flash, redirect, render_template, session, url_for

from app.login import blueprint
from app.login.forms import SignInForm, SignUpForm
from app.login.services import (
    EmailVerificationError,
    InvalidEmailOrPassword,
    mail_srv,
    users_srv,
)


@blueprint.route("/signin", methods=("POST", "GET"))
def signin():
    form = SignInForm()
    if not form.is_submitted():
        return render_template("signin.html", form=form, error=None)

    if form.validate():
        error = None
        try:
            users_srv.check_password(form.email.data, form.password.data)
        except InvalidEmailOrPassword:
            error = "The email or password is incorrect"

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
        if users_srv.exists(form.email.data, form.username.data):
            error = "This email or username is already used"
        elif form.password.data != form.confirm.data:
            error = "The confirm password does not match the password"
        else:
            user = users_srv.add(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            token = users_srv.get_email_confirmation_token(user.id)
            verify_url = url_for(
                "login.verify_email", token=token, _external=True
            )
            mail_srv.send(
                _from="noreply-missabrick@lucapalmi.com",
                to=user.email,
                subject="MissABrick - Verify your email",
                content=f"You can verify your email by clicking on this link: {verify_url}",
            )

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
        users_srv.confirm_email(token)
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
