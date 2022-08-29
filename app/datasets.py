import typing
import json
import pandas as pd

PARTS_COLS = ['part_num','color_id','quantity','is_spare','color_name','color_rgb','color_is_trans','part_name','part_cat_id','part_material']
MINIFIGS_PARTS_COLS = ['part_num','color_id','quantity','is_spare','color_name','color_rgb','color_is_trans','part_name','part_cat_id','part_material','fig_num']
ELEMENTS_COLS = ['part_num','color_id','element_id']

def _concat_dataframes(frames: typing.Iterable[pd.DataFrame], columns: list):
    if len(frames) > 0:
        return pd.concat(frames)

    return pd.DataFrame(columns=columns)

def _get_inventories(set_number: str):
    inventories = pd.read_csv('./datasets/inventories.csv')

    all_invs = inventories[inventories['set_num'] == set_number]
    invs = all_invs[all_invs['version'] >= all_invs['version'].max()]

    return invs['id']

def _get_inventory_sets(inventories: typing.Iterable[int], quantity: int = 1):
    all_sets_df = pd.read_csv('./datasets/sets.csv')
    inventory_sets_df = pd.read_csv('./datasets/inventory_sets.csv')

    sets = inventory_sets_df[inventory_sets_df['inventory_id'].isin(inventories)].filter(items=['set_num', 'quantity'])
    fsets = sets.join(all_sets_df.set_index('set_num'), on=['set_num'])
    fsets['quantity'] *= quantity
    
    return fsets

def _get_inventory_parts(inventories: typing.Iterable[int], quantity: int = 1):
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
    set_inventories = _get_inventories(set_number)

    _sets = _get_inventory_sets(set_inventories, quantity=quantity)
    _parts, _parts_elements = _get_inventory_parts(set_inventories, quantity=quantity)
    _minifigs = _get_inventory_minifigs(set_inventories, quantity=quantity)

    if not _sets.empty:
        assert _parts.empty, "Set has multiple sub-sets but also contains parts !"
        assert _minifigs.empty, "Set has multiple sub-sets but also contains minifigs !"

        _parts_list = []
        _minifigs_parts_list = []
        _elements_list = []

        for _, _set in _sets.iterrows():
            parts, minifigs_parts, elements = get_set_data(_set['set_num'], quantity=_set['quantity'])
            parts['set_num'] = _set['set_num']
            minifigs_parts['parent_set'] = _set['set_num']
            elements['set_num'] = _set['set_num']

            _parts_list.append(parts)
            _minifigs_parts_list.append(minifigs_parts)
            _elements_list.append(elements)

        return _concat_dataframes(_parts_list, PARTS_COLS), _concat_dataframes(_minifigs_parts_list, MINIFIGS_PARTS_COLS), _concat_dataframes(_elements_list, ELEMENTS_COLS)

    # Get parts for minifigs and concatenate all elements
    _minifigs_parts_list = []
    _minifigs_elements_list = []
    for _, minifig in _minifigs.iterrows():
        _minifigs_inventories = _get_inventories(minifig['fig_num'])
        _minifig_parts, _minifig_elements = _get_inventory_parts(_minifigs_inventories, quantity=minifig['quantity'])
        _minifig_parts['fig_num'] = minifig['fig_num']
        _minifigs_parts_list.append(_minifig_parts)
        _minifigs_elements_list.append(_minifig_elements)
    
    _minifigs_parts = _concat_dataframes(_minifigs_parts_list, MINIFIGS_PARTS_COLS)
    _elements = _concat_dataframes([_parts_elements] + _minifigs_elements_list, ELEMENTS_COLS)

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
    all_sets = pd.read_csv('./datasets/sets.csv')

    filtered_sets = all_sets
    if search is not None or search != '':
        filtered_sets = all_sets[all_sets['set_num'].str.startswith(search)]

    all_themes = pd.read_csv('./datasets/themes.csv')
    sets_with_theme = filtered_sets.join(all_themes.set_index('id').filter(items=['name']), on='theme_id', rsuffix='_theme')
    json_data = json.loads(sets_with_theme.to_json(orient='table'))['data']

    return json_data
