from flask import abort, redirect, render_template, request, session, url_for

from app.catalog import blueprint
from app.catalog.forms import UploadForm
from app.catalog.utils import read_uploaded_set_excel_file, send_temp_file
from app.services import report_srv, sets_srv


@blueprint.route("/")
def index():
    if session.get("authenticated", False) is False:
        return redirect(url_for("catalog.explore"))

    return render_template("index.html")


@blueprint.route("/explore")
def explore():
    page = int(request.args.get("page", 1))
    search = request.args.get("search", "")
    page_size = int(request.args.get("page_size", 20))

    pagination = sets_srv.search(
        search, paginate=True, current_page=page, page_size=page_size
    )
    return render_template(
        "explore.html", search=search, pagination=pagination
    )


@blueprint.route("/download/<set_number>")
def download(set_number: int):
    # get_set_data('9493-1')
    # get_set_data('5006061-1')
    # get_set_data('K8672-1')

    parts, minifigs_parts, elements = sets_srv.get_parts(set_number)
    return send_temp_file(set_number, parts, minifigs_parts, elements)


@blueprint.route("/report", methods=("POST", "GET"))
def report():
    form = UploadForm()
    if form.validate_on_submit():
        (
            parts_df,
            minifigs_parts_df,
            elements_df,
        ) = read_uploaded_set_excel_file(form.file.data)

        # Missing data
        if any(
            map(
                lambda v: v is None, [parts_df, minifigs_parts_df, elements_df]
            )
        ):
            abort(400)

        # Generate report
        set_report = report_srv.generate_report(
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
