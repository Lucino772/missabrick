import pandas as pd
from django.shortcuts import HttpResponse
from functools import reduce

import os

from legoapp.models import (Color, Element, Inventory, InventoryMinifigs,
                            InventoryParts, InventorySets, Minifig, Part,
                            PartsCategory, PartsRelationship, Set, Theme)

def set_exists(set_number: str):
    return Set.objects.count() > 0

def _fetch_inventories_from_sets(set_number: str, quantity: int = 1):
    _set = Set.objects.get(set_num=set_number)
    inv = Inventory.objects.filter(_set=_set).order_by('version').first()
    inv_sets = inv.inventorysets_set.all()

    inventories = [(inv, quantity)]

    for inv_set in inv_sets:
        inventories += _fetch_inventories_from_sets(inv_set._set.set_num, inv_set.quantity * quantity)

    return inventories

def get_set_data(set_number: str, quantity: int = 1):
    invs = _fetch_inventories_from_sets(set_number, quantity)

    parts = []
    fig_parts = []
    for inv_set, _quantity in invs:
        parts.append((
            inv_set._set.set_num, 
            inv_set.inventoryparts_set.all(),
            _quantity
        ))
        for inv_fig in inv_set.inventoryminifigs_set.all():
            fig_parts.append((
                inv_set._set.set_num, 
                inv_fig.minifig.fig_num, 
                inv_fig.inventory.inventoryparts_set.all(), 
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
                _query = inv_part.part.element_set.filter(color=inv_part.color)
                if _query.count() == 0:
                    yield {
                        'set_num': set_num,
                        'part_num': elem.part.part_num,
                        'color_id': elem.color.id,
                        'element_id': None
                    }
                else:
                    for elem in _query.all():
                        yield {
                            'set_num': set_num,
                            'part_num': elem.part.part_num,
                            'color_id': elem.color.id,
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

    _parts = pd.DataFrame(_format_parts(parts))
    _fig_parts = pd.DataFrame(_format_parts(fig_parts))
    _elements = pd.DataFrame(_format_elements(parts + fig_parts))

    return _parts, _fig_parts, _elements

# def _find_first_key(possible_values: typing.Iterable[str], search_list: typing.Iterable[str]):
#     for key in possible_values:
#         if key in search_list:
#             return key

# def gen_report(parts: pd.DataFrame, fig_parts: pd.DataFrame, elements: pd.DataFrame):
#     count_keys = ['count', 'current']
#     parts_count_key = _find_first_key(count_keys, parts.columns)
#     fig_parts_count_key = _find_first_key(count_keys, fig_parts.columns)

#     if parts_count_key is None:
#         parts['count'] = 0
#         parts_count_key = 'count'

#     if fig_parts_count_key is None:
#         fig_parts['count'] = 0
#         fig_parts_count_key = 'count'

#     # Calculate missing pieces
#     parts['missing'] = parts['quantity'] - parts[parts_count_key]
#     fig_parts['missing'] = fig_parts['quantity'] - fig_parts[fig_parts_count_key]


#     parts_data = json.loads(parts.to_json(orient='table')).get('data', [])
#     fig_parts_data = json.loads(fig_parts.to_json(orient='table')).get('data', [])

#     return {
#         'parts': parts_data,
#         'fig_parts': fig_parts_data
#     }

# def search_sets(search: str, current_page: int, page_size: int):
#     _offset = 0 + (page_size * (current_page - 1))
#     with db as conn:
#         cursor = db_utils.execute_script('search_sets.sql', conn, search=search.strip(), page_size=page_size, offset=_offset)
#         cnt = cursor.execute('SELECT total_rows from sets_count').fetchone()
        
#         _last = cnt['total_rows'] // page_size + (0 if cnt['total_rows'] % page_size == 0 else 1)
        
#         _next = current_page + 1
#         if _next > _last:
#             _next = None

#         _prev = current_page - 1
#         if _prev < 1:
#             _prev = None

#         sets = pd.read_sql_query('SELECT * FROM found_sets', conn)

#     return json.loads(sets.to_json(orient='table'))['data'], _next, _prev, _last


def index(request):
    # page = request.args.get('page', 1, type=int)
    # search = request.args.get('search', '', type=str)
    # sets, next_page, prev_page, last_page = search_sets(search, page, 20)
    # return render_template('index.html', sets=sets, current_search=search, current_page=page, prev_page=prev_page, next_page=next_page, last_page=last_page)
    return HttpResponse("Index Page")

def download_set(request):
    if not set_exists('9493-1'):
        pass

    # get_set_data('9493-1')
    get_set_data('5006061-1')
    # get_set_data('K8672-1')

    # parts, minifigs_parts, elements = get_set_data(set_number)
    # fd, filename = create_temp_set_excel_file(parts, minifigs_parts, elements)
    # nbytes = os.stat(filename).st_size

    # return current_app.response_class(
    #     stream_file_and_remove(filename, fd),
    #     headers={
    #         'Content-Disposition': 'attachment', 
    #         'Content-Length': nbytes,
    #         'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    #         'filename': f'{set_number}.xlsx'
    #     }
    # )
    return HttpResponse("Download Set")

def report(request):
    # set_report = None
    # if request.method == 'POST':
    #     file = request.files.get('file', None)
    #     if file is None:
    #         abort(403)
        
    #     parts_df, minifigs_parts_df, elements_df = read_uploaded_set_excel_file(file)

    #     # Missing data
    #     if any(map(lambda v: v is None, [parts_df, minifigs_parts_df, elements_df])):
    #         abort(403)

    #     # Generate report
    #     set_report = gen_report(parts_df, minifigs_parts_df, elements_df)

    # return render_template('report.html', report=set_report)
    return HttpResponse("Report")
