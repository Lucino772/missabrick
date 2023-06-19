from app.controllers.abstract import AbstractController
from app.interfaces.controllers.explore import IExploreController
from app.interfaces.views.explore import IExploreView


class ExploreController(AbstractController[IExploreView], IExploreController):
    def search(self, query: str, current_page: int, page_size: int):
        return super().search(query, current_page, page_size)

    def download(self, set_id: str):
        return super().download(set_id)
