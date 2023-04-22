from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired


class SignUpForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    confirm = PasswordField(validators=[DataRequired()])


class SignInForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
