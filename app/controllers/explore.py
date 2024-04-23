from flask import Blueprint, Request, render_template
from flask.views import MethodView
from injector import inject

from app.extensions import htmx
from app.interfaces.services.export import IExportService
from app.interfaces.services.search import ISearchService
from app.utils import send_file

blueprint = Blueprint("explore", __name__, url_prefix="/explore")


@inject
class IndexView(MethodView):
    def __init__(self, request: Request, search_service: ISearchService):
        self._search_service = search_service
        self._request = request

    def _parse_request(self):
        page = int(self._request.args.get("page", 1))
        query = self._request.args.get("search", "")
        page_size = int(self._request.args.get("page_size", 10))
        return page, query, page_size

    def get(self):
        page, query, page_size = self._parse_request()
        keywords, search = self._search_service.parse_query(query)
        results = self._search_service.search(search, keywords, page, page_size)
        themes = self._search_service.get_themes()
        years = self._search_service.get_years()

        if htmx:
            if htmx.target == "search-result":
                return render_template(
                    "partials/explore/results.html",
                    search=query,
                    pagination=results,
                )
            if htmx.target == "content":
                return render_template(
                    "partials/explore/index.html",
                    search=query,
                    pagination=results,
                    themes=themes,
                    years=years,
                )

        return render_template(
            "explore.html",
            search=query,
            pagination=results,
            themes=themes,
            years=years,
        )


@inject
class DownloadView(MethodView):
    def __init__(self, export_service: IExportService) -> None:
        self._export_service = export_service

    def get(self, set_id: str):
        fd, filename = self._export_service.export_parts(set_id)
        return send_file(
            f"{set_id}.xlsx",
            filename,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            fd,
        )


blueprint.add_url_rule("/", view_func=IndexView.as_view("index"))
blueprint.add_url_rule(
    "/download/<string:set_id>", view_func=DownloadView.as_view("download")
)
