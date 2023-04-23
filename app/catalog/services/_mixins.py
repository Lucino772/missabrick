from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session


class SqlServiceMixin:
    def __init__(self, app: Flask = None, db: SQLAlchemy = None) -> None:
        self.__app = app
        self.__db = db
        if db is not None:
            self.__session: Session = db.session

    def init_app(self, app: Flask, db: SQLAlchemy):
        self.__app = app
        self.__db = db
        self.__session: Session = db.session

    @property
    def app(self):
        return self.__app

    @property
    def db(self):
        return self.__db

    @property
    def session(self):
        return self.__session
