import abc
import datetime as dt

import itsdangerous
import sqlalchemy as sa

from app.login.models import User
from app.login.services import EmailVerificationError, InvalidEmailOrPassword
from app.login.services._mixins import SqlServiceMixin


class AbstractUsersService(abc.ABC):
    @abc.abstractmethod
    def all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, username: str, email: str, password: str):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def exists(self, email: str = None, username: str = None):
        raise NotImplementedError

    @abc.abstractmethod
    def check_password(self, email: str, password: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_email_confirmation_token(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def confirm_email(self, token: str, expiration: int = 3600):
        raise NotImplementedError


class SqlUsersService(AbstractUsersService, SqlServiceMixin):
    def all(self):
        return self.session.execute(sa.select(User)).scalars().all()

    def get(self, id: int):
        return self.session.get(User, id)

    def add(self, username: str, email: str, password: str):
        user = User(username=username, email=email, password=password)
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, id: int):
        user = self.get(id)
        if user is not None:
            self.session.delete(user)
            self.session.commit()

    def exists(self, email: str = None, username: str = None):
        select = sa.select(User)
        if email is not None and username is not None:
            select = select.filter(
                User.email == email or User.username == username
            )
        elif email is not None:
            select = select.filter(User.email == email)
        elif username is not None:
            select = select.filter(User.username == username)
        else:
            return False

        return self.session.execute(select).scalars().first() is not None

    def check_password(self, email: str, password: str):
        user = (
            self.session.execute(sa.select(User).filter(User.email == email))
            .scalars()
            .first()
        )
        if user is None:
            raise InvalidEmailOrPassword()

        if user.password != password:
            raise InvalidEmailOrPassword()

    def _get_serializer(self):
        return itsdangerous.URLSafeTimedSerializer(
            secret_key=self.app.config["SECRET_KEY"],
            salt=self.app.config["SECURITY_PASSWORD_SALT"],
        )

    def get_email_confirmation_token(self, id: int):
        user = self.get(id)
        if user is not None:
            return self._get_serializer().dumps(user.email)

    def confirm_email(self, token: str, expiration: int = 3600):
        try:
            email = self._get_serializer().loads(token, max_age=expiration)
            user = (
                self.session.execute(
                    sa.select(User).filter(User.email == email)
                )
                .scalars()
                .first()
            )
            if user is None:
                raise EmailVerificationError(invalid_email=True)

            user.email_verified = True
            user.email_verified_on = dt.datetime.now()
            self.session.add(user)
            self.session.commit()
        except itsdangerous.SignatureExpired:
            raise EmailVerificationError(timeout=True)
        except itsdangerous.BadSignature:
            raise EmailVerificationError()
