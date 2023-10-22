from injector import Binder, Module

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


class ServiceModule(Module):
    def __init__(self, app):
        self._app = app

    def configure(self, binder: Binder) -> None:
        binder.bind(IExportService, to=ExportService)
        binder.bind(IMailService, to=MailService)
        binder.bind(IReportService, to=ReportService)
        binder.bind(ISearchService, to=SearchService)
        binder.bind(IAuthenticationService, to=AuthenticationService)
        binder.bind(IAccountService, to=AccountService)
        binder.bind(ISigningService, to=SigningService)
