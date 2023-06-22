import typing as t

from app.interfaces.daos.dao import Dao
from app.models.orm.lego import GenericSetRelationship


class IGenericSetRelationshipDao(
    Dao[GenericSetRelationship, t.Tuple[str, str]]
):
    ...
