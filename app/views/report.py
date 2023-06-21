from flask import Blueprint

from app.factory.controller import ControllerFactory
from app.interfaces.controllers.report import IReportController
from app.interfaces.views.report import IReportView
from app.views.abstract import AbstractView


class ReportView(AbstractView[IReportController], IReportView):
    controller_factory = ControllerFactory().get_report_controller

    def generate(self):
        return self.controller.generate()

    def as_blueprint(self):
        report_bp = Blueprint("report", __name__, url_prefix="/report")
        report_bp.add_url_rule(
            "/", view_func=self.generate, methods=["GET", "POST"]
        )
        return report_bp
