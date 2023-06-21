from flask import Blueprint, render_template, request

from app.factories import service_factory
from app.utils import send_file

blueprint = Blueprint("explore", __name__, url_prefix="/explore")


@blueprint.route("/")
def index():
    page = int(request.args.get("page", 1))
    query = request.args.get("search", "")
    page_size = int(request.args.get("page_size", 10))

    search_service = service_factory.get_search_service()
    keywords, search = search_service.parse_query(query)
    results = search_service.search(search, keywords, page, page_size)
    themes = search_service.get_themes()
    years = search_service.get_years()

    return render_template(
        "explore.html",
        search=query,
        pagination=results,
        themes=themes,
        years=years,
    )


@blueprint.route("/download/<string:set_id>")
def download(set_id: str):
    export_service = service_factory.get_export_service()

    fd, filename = export_service.export_parts(set_id)
    return send_file(
        f"{set_id}.xlsx",
        filename,
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        fd,
    )
