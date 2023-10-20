import typing as t

from flask import current_app

from app.interfaces.factory.service import IServiceFactory
from app.services.account import AccountService
from app.services.authentication import AuthenticationService
from app.services.export import ExportService
from app.services.mail import MailService
from app.services.report import ReportService
from app.services.search import SearchService
from app.services.signing import SigningService

if t.TYPE_CHECKING:
    from app.interfaces.services.account import IAccountService
    from app.interfaces.services.authentication import IAuthenticationService
    from app.interfaces.services.export import IExportService
    from app.interfaces.services.mail import IMailService
    from app.interfaces.services.report import IReportService
    from app.interfaces.services.search import ISearchService
    from app.interfaces.services.signing import ISigningService


class ServiceFactory(IServiceFactory):
    def get_export_service(self) -> "IExportService":
        return ExportService()

    def get_mail_service(self) -> "IMailService":
        return MailService()

    def get_report_service(self) -> "IReportService":
        return ReportService()

    def get_search_service(self) -> "ISearchService":
        return SearchService()

    def get_authentication_service(self) -> "IAuthenticationService":
        return AuthenticationService()

    def get_account_service(self) -> "IAccountService":
        return AccountService()

    def get_signing_service(self) -> "ISigningService":
        return SigningService(
            current_app.config["SECRET_KEY"],
            current_app.config["SECURITY_PASSWORD_SALT"],
        )
