from flask_sqlalchemy import SQLAlchemy
from injector import Binder, Module, singleton
from sqlalchemy.orm import scoped_session


class DBModule(Module):
    def __init__(self, app, db):
        self._app = app
        self._db = db

    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, to=self._db, scope=singleton)
        binder.bind(scoped_session, to=self._db.session, scope=singleton)
