import json
import os
import tempfile
import typing

import pandas as pd
from django import forms
from django.core.files.temp import NamedTemporaryFile
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import HttpResponse, render

from legoapp.models import Inventory, Set


# Forms
class UploadReportForm(forms.Form):
    file = forms.FileField()

# DB
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
                inv_fig.minifig.inventory_set.order_by('version').first().inventoryparts_set.all(),
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
    sets_qs = Set.objects.filter(set_num__contains=search.strip())
    paginator = Paginator(sets_qs, page_size)
    page = paginator.page(current_page)

    return (
        page.object_list, 
        page.next_page_number() if page.has_next() else None,
        page.previous_page_number() if page.has_previous() else None,
        paginator.num_pages
    )

# Utils
def send_temp_file(set_number: str, parts: pd.DataFrame, fig_parts: pd.DataFrame, elements: pd.DataFrame):
    fp = NamedTemporaryFile()
    with pd.ExcelWriter(fp.name, engine="openpyxl") as writer:
        parts.to_excel(writer, sheet_name='parts', index=False)
        fig_parts.to_excel(writer, sheet_name='minifigs', index=False)
        elements.to_excel(writer, sheet_name='elements', index=False)

    nbytes = os.stat(fp.name).st_size
    with open(fp.name, 'rb') as fp:
        response = HttpResponse(fp.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'inline; filename={}'.format(f'{set_number}.xlsx')
        response['Content-Length'] = nbytes
        response['filename'] = f'{set_number}.xlsx'

    os.unlink(fp.name)
    return response

def read_uploaded_set_excel_file(file):
    dataframes = {}
    with tempfile.NamedTemporaryFile() as fp:
        for chunk in file.chunks():
            fp.write(chunk)

        dataframes = pd.read_excel(fp, sheet_name=["parts", "minifigs", "elements"])

    parts_df = dataframes.get('parts', None)
    minifigs_parts_df = dataframes.get('minifigs', None)
    elements_df = dataframes.get('elements', None)

    return parts_df, minifigs_parts_df, elements_df

# Views
def index(request: HttpRequest):
    page = request.GET.get('page', 1)
    search = request.GET.get('search', '')
    sets, next_page, prev_page, last_page = search_sets(search, page, 20)

    return render(request, 'index.html', context={
        'sets': sets,
        'current_search': search,
        'current_page': page,
        'prev_page': prev_page,
        'next_page': next_page,
        'last_page': last_page
    })

def download_set(request: HttpRequest, set_number: str):
    # get_set_data('9493-1')
    # get_set_data('5006061-1')
    # get_set_data('K8672-1')

    parts, minifigs_parts, elements = get_set_data(set_number)
    return send_temp_file(set_number, parts, minifigs_parts, elements)

def report(request: HttpRequest):
    if request.method == 'POST':
        form = UploadReportForm(request.POST, request.FILES)
        if form.is_valid():
            parts_df, minifigs_parts_df, elements_df = read_uploaded_set_excel_file(request.FILES.get('file'))
            
            # Missing data
            if any(map(lambda v: v is None, [parts_df, minifigs_parts_df, elements_df])):
                return HttpResponseBadRequest()

            # Generate report
            set_report = gen_report(parts_df, minifigs_parts_df, elements_df)
            
            return render(request, 'report.html', context={
                'parts': set_report['parts'],
                'fig_parts': set_report['fig_parts'],
                'form': form
            })
    else:
        form = UploadReportForm()
        return render(request, 'report.html', context={
            'parts': [],
            'fig_parts': [],
            'form': form
        })
