import os
from flask import render_template, request, abort, current_app
from app.main import main

from app.datasets import gen_report, get_set_data, set_exists, search_sets
from app.utils import create_temp_set_excel_file, stream_file_and_remove, read_uploaded_set_excel_file

@main.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    sets, next_page, prev_page, last_page = search_sets(search, page, 20)
    return render_template('index.html', sets=sets, current_search=search, current_page=page, prev_page=prev_page, next_page=next_page, last_page=last_page)


@main.route('/download/<set_number>', methods=['GET'])
def download_set(set_number: str):
    if not set_exists(set_number):
        abort(404)

    parts, minifigs_parts, elements = get_set_data(set_number)
    fd, filename = create_temp_set_excel_file(parts, minifigs_parts, elements)
    nbytes = os.stat(filename).st_size

    return current_app.response_class(
        stream_file_and_remove(filename, fd),
        headers={
            'Content-Disposition': 'attachment', 
            'Content-Length': nbytes,
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'filename': f'{set_number}.xlsx'
        }
    )


@main.route('/report', methods=['GET', 'POST'])
def report():
    set_report = None
    if request.method == 'POST':
        file = request.files.get('file', None)
        if file is None:
            abort(403)
        
        parts_df, minifigs_parts_df, elements_df = read_uploaded_set_excel_file(file)

        # Missing data
        if any(map(lambda v: v is None, [parts_df, minifigs_parts_df, elements_df])):
            abort(403)

        # Generate report
        set_report = gen_report(parts_df, minifigs_parts_df, elements_df)

    return render_template('report.html', report=set_report)
