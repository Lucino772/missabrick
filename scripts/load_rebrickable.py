import contextlib
import csv
import gzip
import os
import shutil
import tempfile

import requests

from legoapp.models import (
    Color, 
    Element, 
    Inventory, 
    InventoryMinifigs,
    InventoryParts, 
    InventorySets, 
    Minifig, 
    Part,
    PartsCategory,
    PartsRelationship,
    Set,
    Theme
)


def _donwload_gzip_file(url: str, dest: str):
    response = requests.get(url, stream=True)
    with open(dest, 'wb') as dest_fp:
        with gzip.open(response.raw, 'rb') as data:
            dest_fp.write(data.read())

def _get_files_dest(directory: str, url: str):
    return os.path.join(directory, os.path.splitext(os.path.basename(url))[0])

@contextlib.contextmanager
def _read_csv(filename: str):
    with open(filename, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader)

        yield reader

def _get_default(model, key: str, value, default = None):
    try:
        return model.objects.get(**{ key: value })
    except model.DoesNotExist:
        return default

def _import_themes(filename: str):
    with _read_csv(filename) as reader:
        Theme.objects.all().delete()
        themes = {
            int(row[0]): (Theme(
                id=int(row[0]),
                name=row[1],
                parent=None
            ), row[2])
            for row in reader
        }

        for theme, parent_id in themes.values():
            if parent_id.isnumeric():
                theme.parent = themes[int(parent_id)][0]

        Theme.objects.bulk_create([theme for theme, parent_id in themes.values()])

def _import_colors(filename: str):
    with _read_csv(filename) as reader:
        Color.objects.all().delete()
        colors = [
            Color(
                id=int(row[0]),
                name=row[1],
                rgb=row[2],
                is_trans=(row[3] == 't')
            )
            for row in reader
        ]
        Color.objects.bulk_create(colors)

def _import_part_categories(filename: str):
    with _read_csv(filename) as reader:
        PartsCategory.objects.all().delete()
        categories = [
            PartsCategory(
                id=int(row[0]),
                name=row[1],
            )
            for row in reader
        ]
        PartsCategory.objects.bulk_create(categories)

def _import_parts(filename: str):
    with _read_csv(filename) as reader:
        Part.objects.all().delete()
        parts = [
            Part(
                part_num=row[0],
                name=row[1],
                part_category=PartsCategory.objects.get(id=int(row[2])),
                part_material=row[3],
            )
            for row in reader
        ]
        Part.objects.bulk_create(parts)

def _import_part_relationships(filename: str):
    with _read_csv(filename) as reader:
        PartsRelationship.objects.all().delete()
        relationships = [
            PartsRelationship(
                rel_type=row[0],
                child_part=Part.objects.get(part_num=row[1]),
                parent_part=Part.objects.get(part_num=row[2])
            )
            for row in reader
        ]
        PartsRelationship.objects.bulk_create(relationships)

def _import_elements(filename: str):
    with _read_csv(filename) as reader:
        Element.objects.all().delete()

        elements = [
            Element(
                element_id=int(row[0]),
                part=_get_default(Part, 'part_num', row[1]),
                color=Color.objects.get(id=int(row[2]))
            )
            for row in reader
        ]
        Element.objects.bulk_create(elements)

def _import_minifigs(filename: str):
    with _read_csv(filename) as reader:
        Minifig.objects.all().delete()
        minifigs = [
            Minifig(
                fig_num=row[0],
                name=row[1],
                num_parts=int(row[2]),
                img_url=row[3]
            )
            for row in reader
        ]
        Minifig.objects.bulk_create(minifigs)

def _import_sets(filename: str):
    with _read_csv(filename) as reader:
        Set.objects.all().delete()
        sets = [
            Set(
                set_num=row[0],
                name=row[1],
                year=int(row[2]),
                theme=Theme.objects.get(id=int(row[3])),
                num_parts=int(row[4]),
                img_url=row[5]
            )
            for row in reader
        ]
        Set.objects.bulk_create(sets)

def _import_inventories(filename: str):
    with _read_csv(filename) as reader:
        Inventory.objects.all().delete()
        inventories = [
            Inventory(
                id=int(row[0]),
                version=int(row[1]),
                is_minifig = row[2].startswith('fig-'),
                _set=Set.objects.get(set_num=row[2]) if not row[2].startswith('fig-') else None,
                minifig=Minifig.objects.get(fig_num=row[2]) if row[2].startswith('fig-') else None,
            )
            for row in reader
        ]
        Inventory.objects.bulk_create(inventories)

def _import_inventory_minifigs(filename: str):
    with _read_csv(filename) as reader:
        InventoryMinifigs.objects.all().delete()

        inventories = [
            InventoryMinifigs(
                inventory=_get_default(Inventory, 'id', int(row[0])),
                minifig=Minifig.objects.get(fig_num=row[1]),
                quantity=int(row[2])
            )
            for row in reader
        ]
        InventoryMinifigs.objects.bulk_create(inventories)

def _import_inventory_parts(filename: str):
    with _read_csv(filename) as reader:
        InventoryParts.objects.all().delete()

        inventories = [
            InventoryParts(
                inventory=_get_default(Inventory, 'id', int(row[0])),
                part=Part.objects.get(part_num=row[1]),
                color=Color.objects.get(id=int(row[2])),
                quantity=int(row[3]),
                is_spare=row[4] == 't',
                img_url=row[5]
            )
            for row in reader
        ]
        InventoryParts.objects.bulk_create(inventories)

def _import_inventory_sets(filename: str):
    with _read_csv(filename) as reader:
        InventorySets.objects.all().delete()

        inventories = [
            InventorySets(
                inventory=_get_default(Inventory, 'id', int(row[0])),
                _set=_get_default(Set, 'set_num', row[1]),
                quantity=int(row[2])
            )
            for row in reader
        ]

        InventorySets.objects.bulk_create(inventories)


_DATA_URLS = [
    ('https://cdn.rebrickable.com/media/downloads/themes.csv.gz', _import_themes),
    ('https://cdn.rebrickable.com/media/downloads/colors.csv.gz', _import_colors),
    ('https://cdn.rebrickable.com/media/downloads/part_categories.csv.gz', _import_part_categories),
    ('https://cdn.rebrickable.com/media/downloads/parts.csv.gz', _import_parts),
    ('https://cdn.rebrickable.com/media/downloads/part_relationships.csv.gz', _import_part_relationships),
    ('https://cdn.rebrickable.com/media/downloads/elements.csv.gz', _import_elements),
    ('https://cdn.rebrickable.com/media/downloads/minifigs.csv.gz', _import_minifigs),
    ('https://cdn.rebrickable.com/media/downloads/sets.csv.gz', _import_sets),
    ('https://cdn.rebrickable.com/media/downloads/inventories.csv.gz', _import_inventories),
    ('https://cdn.rebrickable.com/media/downloads/inventory_minifigs.csv.gz', _import_inventory_minifigs),
    ('https://cdn.rebrickable.com/media/downloads/inventory_parts.csv.gz', _import_inventory_parts),
    ('https://cdn.rebrickable.com/media/downloads/inventory_sets.csv.gz', _import_inventory_sets),
]


def run():
    directory = ''
    try:
        directory = tempfile.mkdtemp()

        for url, _import in _DATA_URLS:
            filename = _get_files_dest(directory, url)
            _donwload_gzip_file(url, filename)
            print('Downloaded file {} ({})'.format(filename, url))

            print('Importing data from {}'.format(filename))
            _import(filename)
    finally:
        if os.path.exists(directory):
            shutil.rmtree(directory)
