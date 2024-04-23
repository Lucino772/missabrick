import datetime as dt
from typing import Annotated

from sqlalchemy import DateTime, String
from sqlalchemy.orm import mapped_column
from sqlalchemy_utils import EmailType, PasswordType

intpk = Annotated[int, mapped_column(primary_key=True)]
strpk = Annotated[str, mapped_column(String(20), primary_key=True)]
unique_email = Annotated[str, mapped_column(EmailType(), unique=True)]
pbkdf2_sha512_password = Annotated[
    str, mapped_column(PasswordType(schemes=["pbkdf2_sha512"]))
]
datetime_tz = Annotated[dt.datetime, mapped_column(DateTime(timezone=True))]
