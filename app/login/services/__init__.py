from app.login.services._exceptions import (
    EmailVerificationError,
    InvalidEmailOrPassword,
)
from app.login.services.mail import SendGridMailService
from app.login.services.users import SqlUsersService

users_srv = SqlUsersService()
mail_srv = SendGridMailService()
