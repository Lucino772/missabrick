from injector import Binder, Module

from app.interfaces.daos.color import IColorDao
from app.interfaces.daos.element import IElementDao
from app.interfaces.daos.generic_set import IGenericSetDao
from app.interfaces.daos.generic_set_part import IGenericSetPartDao
from app.interfaces.daos.generic_set_rel import IGenericSetRelationshipDao
from app.interfaces.daos.part import IPartDao
from app.interfaces.daos.part_category import IPartCategoryDao
from app.interfaces.daos.theme import IThemeDao
from app.interfaces.daos.user import IUserDao
from app.interfaces.daos.year import IYearDao
from app.models.dao.lego import (
    ColorDao,
    ElementDao,
    GenericSetDao,
    GenericSetPartDao,
    GenericSetRelationshipDao,
    PartCategoryDao,
    PartDao,
    ThemeDao,
    YearDao,
)
from app.models.dao.login import UserDao


class DAOModule(Module):
    def __init__(self, app):
        self._app = app

    def configure(self, binder: "Binder") -> None:
        binder.bind(IColorDao, to=ColorDao)
        binder.bind(IElementDao, to=ElementDao)
        binder.bind(IGenericSetPartDao, to=GenericSetPartDao)
        binder.bind(IGenericSetRelationshipDao, to=GenericSetRelationshipDao)
        binder.bind(IGenericSetDao, to=GenericSetDao)
        binder.bind(IPartCategoryDao, to=PartCategoryDao)
        binder.bind(IPartDao, to=PartDao)
        binder.bind(IThemeDao, to=ThemeDao)
        binder.bind(IYearDao, to=YearDao)
        binder.bind(IUserDao, to=UserDao)
