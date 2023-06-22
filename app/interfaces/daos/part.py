from app.interfaces.daos.dao import Dao
from app.models.orm.lego import Part


class IPartDao(Dao[Part, str]):
    ...
