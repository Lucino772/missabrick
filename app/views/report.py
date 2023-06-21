from flask import Blueprint

from app.factories import controller_factory
from app.interfaces.controllers.report import IReportController
from app.interfaces.views.report import IReportView
from app.views.abstract import AbstractView


class ReportView(AbstractView[IReportController], IReportView):
    controller_factory = controller_factory.get_report_controller

    def generate(self):
        return self.controller.generate()

    def as_blueprint(self):
        report_bp = Blueprint("report", __name__, url_prefix="/report")
        report_bp.add_url_rule(
            "/", view_func=self.generate, methods=["GET", "POST"]
        )
        return report_bp
