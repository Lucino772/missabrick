from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.orm.base import Base
from app.models.orm.types import (
    datetime_tz,
    intpk,
    pbkdf2_sha512_password,
    unique_email,
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]  # noqa: A003
    username: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[unique_email]
    password: Mapped[pbkdf2_sha512_password]
    email_verified: Mapped[bool] = mapped_column(default=False)
    email_verified_on: Mapped[datetime_tz | None]
