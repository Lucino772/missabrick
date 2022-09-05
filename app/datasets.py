import typing
import json
import pandas as pd

from app import db

def set_exists(set_number: str):
    with db as conn:
        res = (
            conn.cursor()
                .execute(f'''
                    SELECT COUNT(*) AS cnt
                    FROM sets
                    WHERE set_num = '{set_number}'
                ''')
                .fetchone()
        )
    
    return res['cnt'] > 0

def get_set_data(set_number: str, quantity: int = 1):
    with open('./app/database/scripts/fetch_set_data.sql.template', 'r') as fp:
        script = fp.read()

    with db as conn:
        conn.executescript(script.format(set_number=set_number, quantity=quantity))

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

def search_sets(search):
    with db as conn:
        if search:
            query = f'''
                SELECT *
                FROM sets, themes
                WHERE sets.set_num = '{search}'
                    AND themes.id = sets.theme_id
            '''
        else:
            query = '''
                SELECT *
                FROM sets, themes
                WHERE themes.id = sets.theme_id
            '''

        sets = pd.read_sql_query(query, conn)

    return json.loads(sets.to_json(orient='table'))['data']
