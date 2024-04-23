from tempfile import NamedTemporaryFile

import pandas as pd
from flask import Blueprint, abort, render_template
from flask.views import MethodView
from injector import inject
from werkzeug.datastructures import FileStorage

from app.extensions import htmx
from app.forms.report import UploadForm
from app.interfaces.services.report import IReportService

blueprint = Blueprint("report", __name__, url_prefix="/report")


@inject
class GenerateReportView(MethodView):
    def __init__(self, report_service: IReportService):
        self._report_service = report_service
        self._form = UploadForm()

    def _read_uploaded_set_excel_file(self, file: FileStorage):
        dataframes = {}
        with NamedTemporaryFile() as fp:
            file.save(fp)

            dataframes = pd.read_excel(fp, sheet_name=["parts", "minifigs", "elements"])

        parts_df = dataframes.get("parts", None)
        minifigs_parts_df = dataframes.get("minifigs", None)
        elements_df = dataframes.get("elements", None)

        return parts_df, minifigs_parts_df, elements_df

    def get(self):
        if htmx and htmx.target == "content":
            return render_template(
                "partials/report/index.html",
                parts=[],
                fig_parts=[],
                form=self._form,
            )

        return render_template("report.html", parts=[], fig_parts=[], form=self._form)

    def post(self):
        if self._form.validate_on_submit():
            (
                parts_df,
                minifigs_parts_df,
                elements_df,
            ) = self._read_uploaded_set_excel_file(self._form.file.data)

            # Missing data
            if any(v is None for v in [parts_df, minifigs_parts_df, elements_df]):
                abort(400)

            # Generate report
            set_report = self._report_service.generate_report(
                parts_df, minifigs_parts_df, elements_df
            )

            if htmx and htmx.target == "upload-result":
                return render_template(
                    "partials/report/results.html",
                    parts=set_report["parts"],
                    fig_parts=set_report["fig_parts"],
                    form=self._form,
                )

            return render_template(
                "report.html",
                parts=set_report["parts"],
                fig_parts=set_report["fig_parts"],
                form=self._form,
            )
        return render_template("report.html", parts=[], fig_parts=[], form=self._form)


blueprint.add_url_rule("/", view_func=GenerateReportView.as_view("geenrate"))
