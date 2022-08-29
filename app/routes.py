from flask import Blueprint, jsonify, render_template, request, abort, current_app
import os
from .datasets import gen_report, get_set_data, set_exists
from .utils import create_temp_set_excel_file, stream_file_and_remove, read_uploaded_set_excel_file

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app_routes.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file', None)
    if file is None:
        abort(403)
    
    parts_df, minifigs_parts_df, elements_df = read_uploaded_set_excel_file(file)

    # Missing data
    if any(map(lambda v: v is None, [parts_df, minifigs_parts_df, elements_df])):
        abort(403)

    # Generate report
    report = gen_report(parts_df, minifigs_parts_df, elements_df)
    return jsonify(report)

@app_routes.route('/set/<set_number>/file', methods=['GET'])
def get_file(set_number: str):
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
