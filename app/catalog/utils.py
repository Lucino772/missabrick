import typing as t
from app.database import db
from app.catalog.models import Set, Inventory
from flask import current_app

import sqlalchemy as sa
import pandas as pd
import json

from werkzeug.datastructures import FileStorage


import os
from tempfile import NamedTemporaryFile, mkstemp

# DB
def set_exists(set_number: str):
    stmt = (
        sa.select(sa.func.count()).select_from(sa.select(Set).filter_by(set_num=set_number).subquery())
    )
    return db.session.execute(stmt).scalar_one() > 0

def _fetch_inventories_from_sets(set_number: str, quantity: int = 1):
    _set: Set = db.session.execute(
        sa.select(Set).filter_by(set_num=set_number)
    ).scalar_one()
    inv: Inventory = db.session.execute(
        sa.select(Inventory).filter_by(set_id=_set.set_num).order_by(Inventory.version)
    ).scalar_one()

    inventories = [(inv, quantity)]
    for inv_set in inv.inventory_sets:
        inventories += _fetch_inventories_from_sets(inv_set._set.set_num, inv_set.quantity * quantity)

    return inventories

def get_set_data(set_number: str, quantity: int = 1):
    invs = _fetch_inventories_from_sets(set_number, quantity)

    parts = []
    fig_parts = []
    for inv_set, _quantity in invs:
        parts.append((
            inv_set._set.set_num, 
            inv_set.inventory_parts,
            _quantity
        ))
        for inv_fig in inv_set.inventory_minifigs:
            fig_parts.append((
                inv_set._set.set_num, 
                inv_fig.minifig.fig_num,
                db.session.execute(inv_fig.minifig.inventories.order_by('version')).scalar_one().inventory_parts,
                _quantity * inv_fig.quantity
            ))

    def _format_elements(_list):
        for _tuple in _list:
            if len(_tuple) == 3:
                set_num, inv_parts, qty = _tuple
                fig_num = None
            else:
                set_num, fig_num, inv_parts, qty = _tuple

            for inv_part in inv_parts:
                results = list(db.session.execute(inv_part.part.elements.filter_by(color=inv_part.color)).scalars())
                if len(results) == 0:
                    yield {
                        'set_num': set_num,
                        'part_num': inv_part.part.part_num,
                        'color_id': inv_part.color.id,
                        'element_id': None
                    }
                else:
                    for elem in results:
                        yield {
                            'set_num': set_num,
                            'part_num': inv_part.part.part_num,
                            'color_id': inv_part.color.id,
                            'element_id': elem.element_id
                        }

    def _format_parts(_list):
        for _tuple in _list:
            if len(_tuple) == 3:
                set_num, inv_parts, qty = _tuple
                fig_num = None
            else:
                set_num, fig_num, inv_parts, qty = _tuple

            for inv_part in inv_parts:
                item = {
                    'set_num': set_num,
                    'part_num': inv_part.part.part_num,
                    'part_name': inv_part.part.name,
                    'part_material': inv_part.part.part_material,
                    'color_id': inv_part.color.id,
                    'color_name': inv_part.color.name,
                    'color_rgb': inv_part.color.rgb,
                    'color_is_trans': inv_part.color.is_trans,
                    'is_spare': inv_part.is_spare,
                    'img_url': inv_part.img_url,
                    'quantity': inv_part.quantity * qty 
                }
                if fig_num is not None:
                    item['fig_num'] = fig_num

                yield item

    _parts = pd.DataFrame(_format_parts(parts), columns=['set_num', 'part_num', 'part_name', 'part_material', 'color_id', 'color_name', 'color_rgb', 'color_is_trans', 'is_spare', 'img_url', 'quantity'])
    _fig_parts = pd.DataFrame(_format_parts(fig_parts), columns=['set_num', 'fig_num', 'part_num', 'part_name', 'part_material', 'color_id', 'color_name', 'color_rgb', 'color_is_trans', 'is_spare', 'img_url', 'quantity'])
    _elements = pd.DataFrame(_format_elements(parts + fig_parts), columns=['set_num', 'part_num', 'color_id', 'element_id'])

    return _parts, _fig_parts, _elements

def _find_first_key(possible_values: t.Iterable[str], search_list: t.Iterable[str]):
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
    page = db.paginate(
        sa.select(Set).filter(Set.set_num.contains(search.strip())).order_by(Set.year),
        page=current_page,
        per_page=page_size
    )

    return page

# Web
def stream_file_and_remove(filename: str, fd: int = None):
    open_path = filename if fd is None else fd

    with open(open_path, 'rb', closefd=True) as fp:
        yield from fp

    os.remove(filename)

def send_temp_file(set_number: str, parts: pd.DataFrame, fig_parts: pd.DataFrame, elements: pd.DataFrame):
    fd, filename = mkstemp()
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        parts.to_excel(writer, sheet_name='parts', index=False)
        fig_parts.to_excel(writer, sheet_name='minifigs', index=False)
        elements.to_excel(writer, sheet_name='elements', index=False)

    nbytes = os.stat(filename).st_size
    return current_app.response_class(
        stream_file_and_remove(filename, fd),
        headers={
            'Content-Disposition': f'inline; filename={set_number}.xlsx', 
            'Content-Length': nbytes,
            'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'filename': f'{set_number}.xlsx'
        }
    )

def read_uploaded_set_excel_file(file: FileStorage):
    dataframes = {}
    with NamedTemporaryFile() as fp:
        file.save(fp)

        dataframes = pd.read_excel(fp, sheet_name=["parts", "minifigs", "elements"])

    parts_df = dataframes.get('parts', None)
    minifigs_parts_df = dataframes.get('minifigs', None)
    elements_df = dataframes.get('elements', None)

    return parts_df, minifigs_parts_df, elements_df
