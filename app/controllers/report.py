from tempfile import NamedTemporaryFile

import pandas as pd
from flask import Blueprint, abort, render_template
from werkzeug.datastructures import FileStorage

from app.factories import service_factory
from app.forms.report import UploadForm

blueprint = Blueprint("report", __name__, url_prefix="/report")


def _read_uploaded_set_excel_file(file: FileStorage):
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


@blueprint.route("/", methods=["GET", "POST"])
def generate():
    form = UploadForm()
    if form.validate_on_submit():
        (
            parts_df,
            minifigs_parts_df,
            elements_df,
        ) = _read_uploaded_set_excel_file(form.file.data)

        # Missing data
        if any(
            map(
                lambda v: v is None,
                [parts_df, minifigs_parts_df, elements_df],
            )
        ):
            abort(400)

        # Generate report
        report_service = service_factory.get_report_service()
        set_report = report_service.generate_report(
            parts_df, minifigs_parts_df, elements_df
        )

        return render_template(
            "report.html",
            parts=set_report["parts"],
            fig_parts=set_report["fig_parts"],
            form=form,
        )
    else:
        return render_template(
            "report.html", parts=[], fig_parts=[], form=form
        )
