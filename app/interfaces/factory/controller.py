import typing as t

from app.interfaces.controllers.explore import IExploreController
from app.interfaces.controllers.login import ILoginController
from app.interfaces.controllers.report import IReportController
from app.interfaces.views.explore import IExploreView
from app.interfaces.views.login import ILoginView
from app.interfaces.views.report import IReportView


class IControllerFactory(t.Protocol):
    @t.overload
    def get_controller(self, view: IExploreView) -> IExploreController:
        ...

    @t.overload
    def get_controller(self, view: ILoginView) -> ILoginController:
        ...

    @t.overload
    def get_controller(self, view: IReportView) -> IReportController:
        ...
