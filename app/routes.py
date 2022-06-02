from flask import Blueprint, redirect, render_template, request, url_for, send_file, jsonify, abort, after_this_request, current_app
import os
import uuid
from .datasets import Set
import pandas as pd

import tempfile


app_routes = Blueprint('app_routes', __name__)


def _create_excel(filename: str, parts: pd.DataFrame, fig_parts: pd.DataFrame, elements: pd.DataFrame):
    with pd.ExcelWriter(filename) as writer:
        parts.to_excel(writer, engine="openpyxl", sheet_name='parts', index=False)
        fig_parts.to_excel(writer, engine="openpyxl", sheet_name='minifigs', index=False)
        elements.to_excel(writer, engine="openpyxl", sheet_name='elements', index=False)

@app_routes.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app_routes.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file', None)
    if file is None:
        return 'ERROR'
    
    dataframes = {}
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(file.stream.read())

        dataframes = pd.read_excel(fp, sheet_name=["parts", "minifigs", "elements"])

    parts_df = dataframes.get('parts', None)
    minifigs_parts_df = dataframes.get('minifigs', None)
    elements_df = dataframes.get('elements', None)

    print(parts_df)
    print(minifigs_parts_df)
    print(elements_df)

    return "HELLO WORLD !"

@app_routes.route('/set/<set_number>/file', methods=['GET'])
def get_file(set_number: str):
    _set = Set(set_number)

    filename = os.path.join(os.getcwd(), 'files', f'{_set.set_num}.xlsx')

    if len(_set.sets) > 0:
        _create_excel(filename, _set.sets.parts, _set.sets.minifigs.parts, _set.sets.elements)
    else:
        _create_excel(filename, _set.parts, _set.minifigs.parts, _set.elements)

    return jsonify(url=url_for('app_routes.download_file', filename=f'{_set.set_num}.xlsx'))

@app_routes.route('/file/download/<filename>')
def download_file(filename: str):
    filepath = os.path.join(os.getcwd(), 'files', filename)

    if not os.path.exists(filepath):
        abort(404)

    def stream_file_and_remove():
        with open(filepath, 'rb') as fp:
            yield from fp
        
        os.remove(filepath)

    return current_app.response_class(
        stream_file_and_remove(),
        headers={'Content-Disposition': 'attachment', 'filename': filename}
    )
