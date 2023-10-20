from app.extensions import db
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


class DaoFactory:
    def get_color_dao(self):
        return ColorDao(db_session=db.session)

    def get_element_dao(self):
        return ElementDao(db_session=db.session)

    def get_generic_set_dao(self):
        return GenericSetDao(db_session=db.session)

    def get_generic_set_part_dao(self):
        return GenericSetPartDao(db_session=db.session)

    def get_generic_set_rel_dao(self):
        return GenericSetRelationshipDao(db_session=db.session)

    def get_part_category_dao(self):
        return PartCategoryDao(db_session=db.session)

    def get_part_dao(self):
        return PartDao(db_session=db.session)

    def get_theme_dao(self):
        return ThemeDao(db_session=db.session)

    def get_year_dao(self):
        return YearDao(db_session=db.session)

    def get_user_dao(self):
        return UserDao(db_session=db.session)
