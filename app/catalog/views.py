from flask import render_template, request, abort
from app.catalog import blueprint

from app.catalog.utils import search_sets, get_set_data, send_temp_file, read_uploaded_set_excel_file, gen_report
from app.catalog.forms import UploadForm

@blueprint.route("/")
def index():
    return render_template("index.html")

@blueprint.route("/explore")
def explore():
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    page_size = int(request.args.get('page_size', 20))

    pagination = search_sets(search, page, page_size)
    return render_template("explore.html", search=search, pagination=pagination)

@blueprint.route("/download/<set_number>")
def download(set_number: int):
    # get_set_data('9493-1')
    # get_set_data('5006061-1')
    # get_set_data('K8672-1')

    parts, minifigs_parts, elements = get_set_data(set_number)
    return send_temp_file(set_number, parts, minifigs_parts, elements)

@blueprint.route("/report", methods=("POST", "GET"))
def report():
    form = UploadForm()
    if form.validate_on_submit():
        parts_df, minifigs_parts_df, elements_df = read_uploaded_set_excel_file(form.file.data)

        # Missing data
        if any(map(lambda v: v is None, [parts_df, minifigs_parts_df, elements_df])):
            abort(400)

        # Generate report
        set_report = gen_report(parts_df, minifigs_parts_df, elements_df)
        return render_template('report.html',
            parts=set_report['parts'],
            fig_parts=set_report['fig_parts'],
            form=form
        )
    else:
        return render_template('report.html',
            parts=[],
            fig_parts=[],
            form=form
        )
