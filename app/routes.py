from flask import Blueprint, jsonify, render_template, request, abort, current_app
import os
from .datasets import gen_report, get_set_data, set_exists, search_sets
from .utils import create_temp_set_excel_file, stream_file_and_remove, read_uploaded_set_excel_file

def paged(_list: list, size: int, current: int):
    if current == 0:
        current = 1

    _last = len(_list) // size + (0 if len(_list) % size == 0 else 1)
    _from, _to = 0 + (size * (current - 1)), size * current
    section = _list[_from:_to]
    
    _next = current + 1
    if _next > _last:
        _next = None

    _prev = current - 1
    if _prev < 1:
        _prev = None

    return section, _next, _prev, _last

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    sets, next_page, prev_page, last_page = paged(search_sets(search), 20, page)
    return render_template('index.html', sets=sets, current_search=search, current_page=page, prev_page=prev_page, next_page=next_page, last_page=last_page)


@app_routes.route('/download/<set_number>', methods=['GET'])
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


@app_routes.route('/report', methods=['GET', 'POST'])
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
