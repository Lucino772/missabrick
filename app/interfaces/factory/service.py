import typing as t

from app.interfaces.services.export import IExportService
from app.interfaces.services.mail import IMailService
from app.interfaces.services.report import IReportService
from app.interfaces.services.search import ISearchService
from app.interfaces.services.user import IUserService


class IServiceFactory(t.Protocol):
    def get_export_service(self) -> IExportService:
        ...

    def get_mail_service(self) -> IMailService:
        ...

    def get_report_service(self) -> IReportService:
        ...

    def get_search_service(self) -> ISearchService:
        ...

    def get_user_service(self) -> IUserService:
        ...
