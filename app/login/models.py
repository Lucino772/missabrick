import sqlalchemy as sa
import sqlalchemy_utils as sa_utils
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        sa.String(20), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        sa_utils.EmailType(), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(
        sa_utils.PasswordType, nullable=False
    )
