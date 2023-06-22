from app.interfaces.daos.dao import Dao
from app.models.orm.lego import GenericSetPart


class IGenericSetPartDao(Dao[GenericSetPart, int]):
    ...
