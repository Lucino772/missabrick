from flask import Blueprint, redirect, render_template, request, url_for, send_file
import os

from .datasets import Set
import pandas as pd


app_routes = Blueprint('app_routes', __name__)

def _create_excel(filename: str, parts: pd.DataFrame, fig_parts: pd.DataFrame, elements: pd.DataFrame):
    with pd.ExcelWriter(filename) as writer:
        parts.to_excel(writer, sheet_name='parts', index=False)
        fig_parts.to_excel(writer, sheet_name='minifigs', index=False)
        elements.to_excel(writer, sheet_name='elements', index=False)


@app_routes.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app_routes.route('/find', methods=['POST'])
def find_set():
    set_number = request.form.get('set_number', None)
    if set_number is None:
        return redirect(url_for('app_routes.index'))

    return redirect(url_for('app_routes.view_set', set_number=set_number))

@app_routes.route('/set/<set_number>', methods=['GET'])
def view_set(set_number: str):
    _set = Set(set_number)

    filename = os.path.join(os.getcwd(), 'files', f'{_set.set_num}.xlsx')
    if len(_set.sets) > 0:
        print('Set {} has multiple sub-sets: {}'.format(_set.set_num, ', '.join([s.set_num for s in _set.sets])))
        print('Creating aggregated file for set {} : {}'.format(_set.set_num, filename))
        _create_excel(filename, _set.sets.parts, _set.sets.minifigs.parts, _set.sets.elements)
    else:
        print('Creating file for set {} : {}'.format(_set.set_num, filename))
        _create_excel(filename, _set.parts, _set.minifigs.parts, _set.elements)

    return send_file(filename)
