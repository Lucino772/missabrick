import typing
import pandas as pd

def _concat_dataframes(frames: typing.Iterable[pd.DataFrame]):
    if len(frames) > 0:
        return pd.concat(frames)

    return pd.DataFrame()

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

        return _concat_dataframes(_parts_list), _concat_dataframes(_minifigs_parts_list), _concat_dataframes(_elements_list)

    # Get parts for minifigs and concatenate all elements
    _minifigs_parts_list = []
    _minifigs_elements_list = []
    for _, minifig in _minifigs.iterrows():
        _minifigs_inventories = _get_inventories(minifig['fig_num'])
        _minifig_parts, _minifig_elements = _get_inventory_parts(_minifigs_inventories, quantity=minifig['quantity'])
        _minifig_parts['fig_num'] = minifig['fig_num']
        _minifigs_parts_list.append(_minifig_parts)
        _minifigs_elements_list.append(_minifig_elements)
    
    _minifigs_parts = _concat_dataframes(_minifigs_parts_list)
    _elements = _concat_dataframes([_parts_elements] + _minifigs_elements_list)

    return _parts, _minifigs_parts, _elements
