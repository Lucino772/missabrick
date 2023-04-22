from flask import redirect, render_template

from app.extensions import db
from app.login import blueprint
from app.login.forms import SignInForm, SignUpForm
from app.login.utils import (
    ConfirmPasswordDoesNotMatch,
    EmailAlreadyTaken,
    UsernameAlreadyTaken,
    check_confirm_password,
    check_email,
    check_username,
    create_user,
    get_user,
)


@blueprint.route("/signin", methods=("POST", "GET"))
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        print(form.data)
    else:
        return render_template("signin.html", form=form)


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
            return redirect("catalog.index")
    else:
        return render_template("signup.html", form=form, error=None), 422
