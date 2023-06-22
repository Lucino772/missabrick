import typing as t

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


class IDaoFactory(t.Protocol):
    def get_color_dao(self) -> "IColorDao":
        ...

    def get_element_dao(self) -> "IElementDao":
        ...

    def get_generic_set_part_dao(self) -> "IGenericSetPartDao":
        ...

    def get_generic_set_rel_dao(self) -> "IGenericSetRelationshipDao":
        ...

    def get_generic_set_dao(self) -> "IGenericSetDao":
        ...

    def get_part_category_dao(self) -> "IPartCategoryDao":
        ...

    def get_part_dao(self) -> "IPartDao":
        ...

    def get_theme_dao(self) -> "IThemeDao":
        ...

    def get_year_dao(self) -> "IYearDao":
        ...

    def get_user_dao(self) -> "IUserDao":
        ...
