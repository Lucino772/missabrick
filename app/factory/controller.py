from app.controllers.explore import ExploreController
from app.controllers.login import LoginController
from app.controllers.report import ReportController
from app.interfaces.controllers.explore import IExploreController
from app.interfaces.controllers.login import ILoginController
from app.interfaces.controllers.report import IReportController
from app.interfaces.factory.controller import IControllerFactory
from app.interfaces.factory.service import IServiceFactory
from app.interfaces.views.view import IView


class ControllerFactory(IControllerFactory):
    def __init__(self, service_factory: IServiceFactory) -> None:
        self.service_factory = service_factory

    def get_explore_controller(self, view: IView) -> IExploreController:
        return ExploreController(view, self.service_factory)

    def get_login_controller(self, view: IView) -> ILoginController:
        return LoginController(view, self.service_factory)

    def get_report_controller(self, view: IView) -> IReportController:
        return ReportController(view, self.service_factory)
