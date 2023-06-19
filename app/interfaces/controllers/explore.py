import typing as t

from app.interfaces.controllers.controller import IController


class IExploreController(IController):
    def search(self, query: str, current_page: int, page_size: int):
        ...

    def download(self, set_id: str):
        ...
