from injector import Binder, Module

from app.interfaces.daos.generic_set import IGenericSetDao
from app.interfaces.daos.theme import IThemeDao
from app.interfaces.daos.user import IUserDao
from app.interfaces.daos.year import IYearDao
from app.models.dao.lego import GenericSetDao, ThemeDao, YearDao
from app.models.dao.login import UserDao


class DAOModule(Module):
    def __init__(self, app):
        self._app = app

    def configure(self, binder: "Binder") -> None:
        binder.bind(IGenericSetDao, to=GenericSetDao)
        binder.bind(IThemeDao, to=ThemeDao)
        binder.bind(IYearDao, to=YearDao)
        binder.bind(IUserDao, to=UserDao)
