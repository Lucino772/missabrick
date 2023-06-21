from app.controllers.explore import ExploreController
from app.controllers.login import LoginController
from app.controllers.report import ReportController
from app.interfaces.controllers.explore import IExploreController
from app.interfaces.controllers.login import ILoginController
from app.interfaces.controllers.report import IReportController
from app.interfaces.factory.controller import IControllerFactory
from app.interfaces.views.view import IView


class ControllerFactory(IControllerFactory):
    def get_explore_controller(self, view: IView) -> IExploreController:
        return ExploreController(view)

    def get_login_controller(self, view: IView) -> ILoginController:
        return LoginController(view)

    def get_report_controller(self, view: IView) -> IReportController:
        return ReportController(view)
