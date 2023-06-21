from app.controllers.abstract import AbstractController
from app.factories import service_factory
from app.interfaces.controllers.explore import IExploreController
from app.interfaces.views.explore import IExploreView


class ExploreController(AbstractController[IExploreView], IExploreController):
    def search(self, query: str, current_page: int, page_size: int):
        search_service = service_factory.get_search_service()

        keywords, search = search_service.parse_query(query)
        results = search_service.search(
            search, keywords, current_page, page_size
        )
        themes = search_service.get_themes()
        years = search_service.get_years()

        return self.view.render(
            "explore.html",
            search=query,
            pagination=results,
            themes=themes,
            years=years,
        )

    def download(self, set_id: str):
        export_service = service_factory.get_export_service()

        fd, filename = export_service.export_parts(set_id)
        return self.view.send_file(
            f"{set_id}.xlsx",
            filename,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            fd,
        )
