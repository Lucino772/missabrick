import typing
import json
import pandas as pd

from app import db
from app.database import utils as db_utils

def set_exists(set_number: str):
    with db as conn:
        res = db_utils.execute_query('set_exists.sql', conn, { 'set_number': set_number }).fetchone()
    
    return res['cnt'] > 0

def get_set_data(set_number: str, quantity: int = 1):
    with db as conn:
        db_utils.execute_script('fetch_set_data.sql.template', conn, set_number=set_number, quantity=quantity)

        _parts = pd.read_sql_query('SELECT * FROM set_parts', conn)
        _minifigs_parts = pd.read_sql_query('SELECT * FROM set_minifigs_parts', conn)
        _elements = pd.read_sql_query('SELECT * FROM set_elements', conn)

    return _parts, _minifigs_parts, _elements

def _find_first_key(possible_values: typing.Iterable[str], search_list: typing.Iterable[str]):
    for key in possible_values:
        if key in search_list:
            return key

def gen_report(parts: pd.DataFrame, fig_parts: pd.DataFrame, elements: pd.DataFrame):
    count_keys = ['count', 'current']
    parts_count_key = _find_first_key(count_keys, parts.columns)
    fig_parts_count_key = _find_first_key(count_keys, fig_parts.columns)

    if parts_count_key is None:
        parts['count'] = 0
        parts_count_key = 'count'

    if fig_parts_count_key is None:
        fig_parts['count'] = 0
        fig_parts_count_key = 'count'

    # Calculate missing pieces
    parts['missing'] = parts['quantity'] - parts[parts_count_key]
    fig_parts['missing'] = fig_parts['quantity'] - fig_parts[fig_parts_count_key]


    parts_data = json.loads(parts.to_json(orient='table')).get('data', [])
    fig_parts_data = json.loads(fig_parts.to_json(orient='table')).get('data', [])

    return {
        'parts': parts_data,
        'fig_parts': fig_parts_data
    }

def search_sets(search: str, current_page: int, page_size: int):
    _offset = 0 + (page_size * (current_page - 1))
    with db as conn:
        cursor = db_utils.execute_script('search_sets.sql', conn, search=search.strip(), page_size=page_size, offset=_offset)
        cnt = cursor.execute('SELECT total_rows from sets_count').fetchone()
        
        _last = cnt['total_rows'] // page_size + (0 if cnt['total_rows'] % page_size == 0 else 1)
        
        _next = current_page + 1
        if _next > _last:
            _next = None

        _prev = current_page - 1
        if _prev < 1:
            _prev = None

        sets = pd.read_sql_query('SELECT * FROM found_sets', conn)

    return json.loads(sets.to_json(orient='table'))['data'], _next, _prev, _last
