from tempfile import NamedTemporaryFile

import pandas as pd
from werkzeug.datastructures import FileStorage

from app.controllers.abstract import AbstractController
from app.forms.report import UploadForm
from app.interfaces.controllers.report import IReportController
from app.interfaces.views.report import IReportView
from app.services.report import ReportService


class ReportController(AbstractController[IReportView], IReportController):
    def _read_uploaded_set_excel_file(self, file: FileStorage):
        dataframes = {}
        with NamedTemporaryFile() as fp:
            file.save(fp)

            dataframes = pd.read_excel(
                fp, sheet_name=["parts", "minifigs", "elements"]
            )

        parts_df = dataframes.get("parts", None)
        minifigs_parts_df = dataframes.get("minifigs", None)
        elements_df = dataframes.get("elements", None)

        return parts_df, minifigs_parts_df, elements_df

    def generate(self):
        form = UploadForm()
        if form.validate_on_submit():
            (
                parts_df,
                minifigs_parts_df,
                elements_df,
            ) = self._read_uploaded_set_excel_file(form.file.data)

            # Missing data
            if any(
                map(
                    lambda v: v is None,
                    [parts_df, minifigs_parts_df, elements_df],
                )
            ):
                self.view.abort(400)

            # Generate report
            report_service = ReportService()
            set_report = report_service.generate_report(
                parts_df, minifigs_parts_df, elements_df
            )

            return self.view.render(
                "report.html",
                parts=set_report["parts"],
                fig_parts=set_report["fig_parts"],
                form=form,
            )
        else:
            return self.view.render(
                "report.html", parts=[], fig_parts=[], form=form
            )
