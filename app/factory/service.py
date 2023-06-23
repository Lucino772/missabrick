from flask import current_app

from app.interfaces.factory.service import IServiceFactory
from app.interfaces.services.account import IAccountService
from app.interfaces.services.authentication import IAuthenticationService
from app.interfaces.services.export import IExportService
from app.interfaces.services.mail import IMailService
from app.interfaces.services.report import IReportService
from app.interfaces.services.search import ISearchService
from app.interfaces.services.signing import ISigningService
from app.services.account import AccountService
from app.services.authentication import AuthenticationService
from app.services.export import ExportService
from app.services.mail import MailService
from app.services.report import ReportService
from app.services.search import SearchService
from app.services.signing import SigningService


class ServiceFactory(IServiceFactory):
    def get_export_service(self) -> IExportService:
        return ExportService(self)

    def get_mail_service(self) -> IMailService:
        return MailService(self)

    def get_report_service(self) -> IReportService:
        return ReportService(self)

    def get_search_service(self) -> ISearchService:
        return SearchService(self)

    def get_authentication_service(self) -> IAuthenticationService:
        return AuthenticationService(self)

    def get_account_service(self) -> IAccountService:
        return AccountService(self)

    def get_signing_service(self) -> ISigningService:
        return SigningService(
            self,
            current_app.config["SECRET_KEY"],
            current_app.config["SECURITY_PASSWORD_SALT"],
        )
