from app.controllers.explore import ExploreController
from app.controllers.login import LoginController
from app.controllers.report import ReportController
from app.interfaces.factory.controller import IControllerFactory
from app.interfaces.views.explore import IExploreView
from app.interfaces.views.login import ILoginView
from app.interfaces.views.report import IReportView


class ControllerFactory(IControllerFactory):
    def get_controller(self, view):
        if isinstance(view, IExploreView):
            return ExploreController(view)
        elif isinstance(view, ILoginView):
            return LoginController(view)
        elif isinstance(view, IReportView):
            return ReportController(view)
        else:
            raise RuntimeError("Invalid view")
