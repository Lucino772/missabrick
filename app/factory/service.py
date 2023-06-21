from app.interfaces.factory.service import IServiceFactory
from app.interfaces.services.export import IExportService
from app.interfaces.services.mail import IMailService
from app.interfaces.services.report import IReportService
from app.interfaces.services.search import ISearchService
from app.interfaces.services.user import IUserService
from app.services.export import ExportService
from app.services.mail import MailService
from app.services.report import ReportService
from app.services.search import SearchService
from app.services.user import UserService


class ServiceFactory(IServiceFactory):
    def get_export_service(self) -> IExportService:
        return ExportService(self)

    def get_mail_service(self) -> IMailService:
        return MailService(self)

    def get_report_service(self) -> IReportService:
        return ReportService(self)

    def get_search_service(self) -> ISearchService:
        return SearchService(self)

    def get_user_service(self) -> IUserService:
        return UserService(self)
