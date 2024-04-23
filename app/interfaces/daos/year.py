from typing import Protocol

from app.interfaces.daos.dao import Dao
from app.models.orm.lego import Year


class IYearDao(Dao[Year, int], Protocol):
    ...
