from flask import current_app

from app.services.account import AccountService
from app.services.authentication import AuthenticationService
from app.services.export import ExportService
from app.services.mail import MailService
from app.services.report import ReportService
from app.services.search import SearchService
from app.services.signing import SigningService


class ServiceFactory:
    def get_export_service(self):
        return ExportService()

    def get_mail_service(self):
        return MailService()

    def get_report_service(self):
        return ReportService()

    def get_search_service(self):
        return SearchService()

    def get_authentication_service(self):
        return AuthenticationService()

    def get_account_service(self):
        return AccountService()

    def get_signing_service(self):
        return SigningService(
            current_app.config["SECRET_KEY"],
            current_app.config["SECURITY_PASSWORD_SALT"],
        )
