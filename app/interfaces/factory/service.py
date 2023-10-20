import typing as t

if t.TYPE_CHECKING:
    from app.interfaces.services.account import IAccountService
    from app.interfaces.services.authentication import IAuthenticationService
    from app.interfaces.services.export import IExportService
    from app.interfaces.services.mail import IMailService
    from app.interfaces.services.report import IReportService
    from app.interfaces.services.search import ISearchService
    from app.interfaces.services.signing import ISigningService


class IServiceFactory(t.Protocol):
    def get_export_service(self) -> "IExportService":
        ...

    def get_mail_service(self) -> "IMailService":
        ...

    def get_report_service(self) -> "IReportService":
        ...

    def get_search_service(self) -> "ISearchService":
        ...

    def get_authentication_service(self) -> "IAuthenticationService":
        ...

    def get_account_service(self) -> "IAccountService":
        ...

    def get_signing_service(self) -> "ISigningService":
        ...
