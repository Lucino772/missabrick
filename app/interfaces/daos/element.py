from app.interfaces.daos.dao import Dao
from app.models.orm.lego import Element


class IElementDao(Dao[Element, int]):
    ...
