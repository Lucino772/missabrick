from app.interfaces.daos.dao import Dao
from app.models.orm.lego import Color


class IColorDao(Dao[Color, int]):
    ...
