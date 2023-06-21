from flask import Blueprint, request

from app.factories import controller_factory
from app.interfaces.controllers.explore import IExploreController
from app.interfaces.views.explore import IExploreView
from app.views.abstract import AbstractView


class ExploreView(AbstractView[IExploreController], IExploreView):
    controller_factory = controller_factory.get_explore_controller

    def index(self):
        page = int(request.args.get("page", 1))
        search = request.args.get("search", "")
        page_size = int(request.args.get("page_size", 10))

        return self.controller.search(search, page, page_size)

    def download(self, set_id: int):
        # get_set_data('9493-1')
        # get_set_data('5006061-1')
        # get_set_data('K8672-1')
        return self.controller.download(set_id)

    def as_blueprint(self):
        explore_bp = Blueprint("explore", __name__, url_prefix="/explore")
        explore_bp.add_url_rule("/", view_func=self.index)
        explore_bp.add_url_rule(
            "/download/<string:set_id>", view_func=self.download
        )
        return explore_bp
