import typing
import json
import pandas as pd

from app import db
from sqlalchemy import text

PARTS_COLS = ['part_num','color_id','quantity','is_spare','color_name','color_rgb','color_is_trans','part_name','part_cat_id','part_material']
MINIFIGS_PARTS_COLS = ['part_num','color_id','quantity','is_spare','color_name','color_rgb','color_is_trans','part_name','part_cat_id','part_material','fig_num']
ELEMENTS_COLS = ['part_num','color_id','element_id']

def _concat_dataframes(frames: typing.Iterable[pd.DataFrame], columns: list):
    if len(frames) > 0:
        return pd.concat(frames)

    return pd.DataFrame(columns=columns)

def _get_inventories(set_number: str):
    with db.get_engine().connect() as conn:
        result = conn.execute(text('''
        WITH tmp_inv AS (
            SELECT * FROM inventories
            WHERE set_num = :set_number
        )
        SELECT * FROM tmp_inv
        WHERE version >= (SELECT MAX(version) from tmp_inv)
        '''), { 'set_number': set_number })

        ids = [item.id for item in result.all()]
        return ids

def _get_inventory_sets(inventories: typing.Iterable[int], quantity: int = 1):
    with db.get_engine().connect() as conn:
        result = conn.execute(text(
        '''
        SELECT sets.*, inventory_sets.quantity
        FROM inventory_sets, sets
        WHERE inventory_sets.inventory_id IN (:inventories) 
              AND inventory_sets.set_num = sets.set_num
        '''
        ), {'inventories': ','.join([str(i) for i in inventories])})
        print(result.all())

    all_sets_df = pd.read_csv('./datasets/sets.csv')
    inventory_sets_df = pd.read_csv('./datasets/inventory_sets.csv')

    sets = inventory_sets_df[inventory_sets_df['inventory_id'].isin(inventories)].filter(items=['set_num', 'quantity'])
    fsets = sets.join(all_sets_df.set_index('set_num'), on=['set_num'])
    fsets['quantity'] *= quantity
    
    return fsets

def _get_inventory_parts(inventories: typing.Iterable[int], quantity: int = 1):
    with db.get_engine().connect() as conn:
        result = conn.execute(text(
        '''
        SELECT p.part_num,
               p.name AS part_name,
               p.part_cat_id,
               p.part_material,
               c.id AS color_id,
               c.name AS color_name,
               c.rgb AS color_rgb,
               c.is_trans AS color_is_trans,
               ip.quantity * :quantity,
               ip.is_spare
        FROM inventory_parts AS ip,
             parts AS p,
             colors AS c
        WHERE ip.inventory_id IN (:inventories)
              AND c.id = ip.color_id
              AND p.part_num = ip.part_num
        '''
        ), {
            'inventories': ','.join([str(i) for i in inventories]),
            'quantity': quantity
        })
        print(result.all())

        result2 = conn.execute(text(
        '''
        WITH tmp AS (
            SELECT p.part_num,
               p.name AS part_name,
               p.part_cat_id,
               p.part_material,
               c.id AS color_id,
               c.name AS color_name,
               c.rgb AS color_rgb,
               c.is_trans AS color_is_trans,
               ip.quantity * :quantity,
               ip.is_spare
            FROM inventory_parts AS ip,
                parts AS p,
                colors AS c
            WHERE ip.inventory_id IN (:inventories)
                AND c.id = ip.color_id
                AND p.part_num = ip.part_num
        )
        SELECT p.part_num, p.color_id, e.element_id
        FROM tmp AS p
        LEFT JOIN elements AS e
              ON p.part_num = e.part_num
              AND p.color_id = e.color_id
        '''
        ), {
            'inventories': ','.join([str(i) for i in inventories]),
            'quantity': quantity
        })
        print(result2.all())

    colors_df = pd.read_csv('./datasets/colors.csv').rename(columns={'name': 'color_name', 'rgb': 'color_rgb', 'is_trans': 'color_is_trans'})
    all_parts_df = pd.read_csv('./datasets/parts.csv').rename(columns={'name': 'part_name'})
    all_elements_df = pd.read_csv('./datasets/elements.csv')
    inventory_parts_df = pd.read_csv('./datasets/inventory_parts.csv')

    # Get all parts from given inventories
    parts = (
        inventory_parts_df[inventory_parts_df['inventory_id'].isin(inventories)]
        .filter(items=['part_num', 'color_id', 'quantity', 'is_spare'])
        .join(colors_df.set_index('id'), on=['color_id'])
        .join(all_parts_df.set_index('part_num'), on=['part_num'])
    ).reset_index(drop=True)
    parts['quantity'] *= quantity

    # Get all elements related to those parts
    elements = (
        parts.filter(items=['part_num', 'color_id'])
        .join(all_elements_df.set_index(['part_num', 'color_id']), on=['part_num', 'color_id'])
    ).reset_index(drop=True)

    return parts, elements

def _get_inventory_minifigs(inventories: typing.Iterable[int], quantity: int = 1):
    all_minifigs_df = pd.read_csv('./datasets/minifigs.csv')
    inventory_minifigs_df = pd.read_csv('./datasets/inventory_minifigs.csv')

    minifigs = inventory_minifigs_df[inventory_minifigs_df['inventory_id'].isin(inventories)].filter(items=['fig_num', 'quantity'])
    fminifigs = minifigs.join(all_minifigs_df.set_index('fig_num'), on=['fig_num'])
    fminifigs['quantity'] *= quantity

    return fminifigs


def set_exists(set_number: str):
    all_sets_df = pd.read_csv('./datasets/sets.csv')
    return (all_sets_df['set_num'] == set_number).any()

def get_set_data(set_number: str, quantity: int = 1):
    with db.get_engine().connect() as conn:
        conn.execute(text(
            '''
            CREATE TEMP TABLE inventory_ids
            AS SELECT id, set_num, :quantity AS quantity
            FROM inventories
            WHERE set_num = :set_number
                 AND version >= (SELECT MAX(version) FROM inventories WHERE set_num = :set_number)
            '''
        ), {'set_number': set_number, 'quantity': quantity })
        conn.execute(text(
            '''
            CREATE TEMP TABLE check_has_sets
            AS SELECT id, quantity FROM inventory_ids
            '''
        ))
        
        check_has_sets_ids = [i.id for i in conn.execute('SELECT * FROM check_has_sets').all()]
        while len(check_has_sets_ids) > 0:
            conn.execute(text(
                '''
                CREATE TEMP TABLE sets_inventories
                AS SELECT inventories.id AS id, sets.set_num AS set_num, inventory_sets.quantity * check_has_sets.quantity AS quantity
                FROM inventory_sets, sets, inventories, check_has_sets
                WHERE inventory_sets.inventory_id = check_has_sets.id 
                    AND inventory_sets.set_num = sets.set_num
                    AND inventories.set_num = sets.set_num
                '''
            ))

            conn.execute(text('INSERT INTO inventory_ids SELECT * FROM sets_inventories'))
            conn.execute(text('DELETE FROM check_has_sets'))
            conn.execute(text('INSERT INTO check_has_sets SELECT id, quantity FROM sets_inventories'))
            conn.execute(text('DROP TABLE sets_inventories'))

            check_has_sets_ids = [i.id for i in conn.execute('SELECT * FROM check_has_sets').all()]

        conn.execute(text(
            '''
            CREATE TEMP TABLE set_parts 
            AS SELECT 
               ids.set_num,
               p.part_num,
               p.name AS part_name,
               p.part_cat_id,
               p.part_material,
               c.id AS color_id,
               c.name AS color_name,
               c.rgb AS color_rgb,
               c.is_trans AS color_is_trans,
               ip.quantity * ids.quantity AS quantity,
               ip.is_spare AS is_spare
            FROM inventory_parts AS ip,
                parts AS p,
                colors AS c,
                inventory_ids AS ids
            WHERE ip.inventory_id = ids.id
                AND c.id = ip.color_id
                AND p.part_num = ip.part_num
            '''
        ))

        conn.execute(text(
            '''
            CREATE TEMP TABLE set_minifigs
            AS SELECT i.id AS id, ids.set_num AS set_num, iv.fig_num, iv.quantity * ids.quantity AS quantity
            FROM inventory_minifigs AS iv,
                 inventories AS i,
                 inventory_ids AS ids
            WHERE iv.inventory_id = ids.id
                AND i.set_num = iv.fig_num 
            '''
        ))

        conn.execute(text(
            '''
            CREATE TEMP TABLE set_minifigs_parts 
            AS SELECT 
               ids.set_num,
               ids.fig_num,
               p.part_num,
               p.name AS part_name,
               p.part_cat_id,
               p.part_material,
               c.id AS color_id,
               c.name AS color_name,
               c.rgb AS color_rgb,
               c.is_trans AS color_is_trans,
               ip.quantity * ids.quantity AS quantity,
               ip.is_spare AS is_spare
            FROM inventory_parts AS ip,
                parts AS p,
                colors AS c,
                set_minifigs AS ids
            WHERE ip.inventory_id = ids.id
                AND c.id = ip.color_id
                AND p.part_num = ip.part_num
            '''
        ))

        _parts = conn.execute('SELECT * FROM set_parts').all()
        _minifigs_parts = conn.execute('SELECT * FROM set_minifigs_parts').all()
        _elements = conn.execute(text(
            '''
            SELECT p.set_num, p.part_num, p.color_id, e.element_id
            FROM set_parts AS p
            LEFT JOIN elements AS e
                 ON p.part_num = e.part_num
                 AND p.color_id = e.color_id
            
            UNION

            SELECT p.set_num, p.part_num, p.color_id, e.element_id
            FROM set_minifigs_parts AS p
            LEFT JOIN elements AS e
                 ON p.part_num = e.part_num
                 AND p.color_id = e.color_id
            '''
        )).all()

    return pd.DataFrame(_parts), pd.DataFrame(_minifigs_parts), pd.DataFrame(_elements)

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
    all_sets = pd.read_csv('./datasets/sets.csv')

    filtered_sets = all_sets
    if search is not None or search != '':
        filtered_sets = all_sets[all_sets['set_num'].str.startswith(search)]

    all_themes = pd.read_csv('./datasets/themes.csv')
    sets_with_theme = filtered_sets.join(all_themes.set_index('id').filter(items=['name']), on='theme_id', rsuffix='_theme')
    json_data = json.loads(sets_with_theme.to_json(orient='table'))['data']

    return json_data
