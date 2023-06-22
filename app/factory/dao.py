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
from app.interfaces.factory.dao import IDaoFactory
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
from app.models.orm.lego import (
    Color,
    Element,
    GenericSet,
    GenericSetPart,
    GenericSetRelationship,
    Part,
    PartCategory,
    Theme,
    Year,
)
from app.models.orm.login import User


class DaoFactory(IDaoFactory):
    def get_color_dao(self) -> IColorDao:
        return ColorDao(Color)

    def get_element_dao(self) -> IElementDao:
        return ElementDao(Element)

    def get_generic_set_dao(self) -> IGenericSetDao:
        return GenericSetDao(GenericSet)

    def get_generic_set_part_dao(self) -> IGenericSetPartDao:
        return GenericSetPartDao(GenericSetPart)

    def get_generic_set_rel_dao(self) -> IGenericSetRelationshipDao:
        return GenericSetRelationshipDao(GenericSetRelationship)

    def get_part_category_dao(self) -> IPartCategoryDao:
        return PartCategoryDao(PartCategory)

    def get_part_dao(self) -> IPartDao:
        return PartDao(Part)

    def get_theme_dao(self) -> IThemeDao:
        return ThemeDao(Theme)

    def get_year_dao(self) -> IYearDao:
        return YearDao(Year)

    def get_user_dao(self) -> IUserDao:
        return UserDao(User)
