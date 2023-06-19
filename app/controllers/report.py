from app.controllers.abstract import AbstractController
from app.interfaces.controllers.report import IReportController
from app.interfaces.views.report import IReportView


class ReportController(AbstractController[IReportView], IReportController):
    def generate(self):
        return super().generate()
