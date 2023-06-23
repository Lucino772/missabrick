from app.interfaces.daos.dao import Dao
from app.models.orm.lego import PartCategory


class IPartCategoryDao(Dao[PartCategory, int]):
    ...
