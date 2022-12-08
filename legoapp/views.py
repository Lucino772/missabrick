from django.shortcuts import HttpResponse
from django.db.models import Max

import os

from legoapp.models import (Color, Element, Inventory, InventoryMinifigs,
                            InventoryParts, InventorySets, Minifig, Part,
                            PartsCategory, PartsRelationship, Set, Theme)

def set_exists(set_number: str):
    return Set.objects.count() > 0

def get_set_data(set_number: str, quantity: int = 1):
    query = """
    WITH RECURSIVE check_set AS (
        SELECT id, set_num, {quantity} AS quantity
        FROM legoapp_inventory
        WHERE set_num = '{set_number}'
            AND version >= (SELECT MAX(version) FROM legoapp_inventory WHERE set_num = '{set_number}')

        UNION

        SELECT legoapp_inventory.id AS id, legoapp_inventory.set_num, legoapp_inventorysets.quantity * {quantity} AS quantity
        FROM legoapp_inventorysets, legoapp_inventory, check_set
        WHERE legoapp_inventorysets.inventory_id = check_set.id
            AND legoapp_inventory.set_num = legoapp_inventorysets.set_num
    )
    SELECT * FROM check_set;
    """.format(quantity=1, set_number=set_number)
    res = Inventory.objects.raw(query)
    print(list(res))

    # with db as conn:
    #     db_utils.execute_script('fetch_set_data.sql.template', conn, set_number=set_number, quantity=quantity)

    #     _parts = pd.read_sql_query('SELECT * FROM set_parts', conn)
    #     _minifigs_parts = pd.read_sql_query('SELECT * FROM set_minifigs_parts', conn)
    #     _elements = pd.read_sql_query('SELECT * FROM set_elements', conn)

    # return _parts, _minifigs_parts, _elements

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
