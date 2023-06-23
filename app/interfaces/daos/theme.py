from app.interfaces.daos.dao import Dao
from app.models.orm.lego import Theme


class IThemeDao(Dao[Theme, int]):
    ...
