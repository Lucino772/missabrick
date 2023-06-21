import typing as t

from app.interfaces.controllers.explore import IExploreController
from app.interfaces.controllers.login import ILoginController
from app.interfaces.controllers.report import IReportController
from app.interfaces.views.view import IView


class IControllerFactory(t.Protocol):
    def get_explore_controller(self, view: IView) -> IExploreController:
        ...

    def get_login_controller(self, view: IView) -> ILoginController:
        ...

    def get_report_controller(self, view: IView) -> IReportController:
        ...
