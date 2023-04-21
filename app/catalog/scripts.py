import contextlib
import csv
import gzip
import os
import shutil
import tempfile
from typing import Any, Callable, Generator, Iterator, List, Type, TypeVar

import requests
from flask.cli import with_appcontext

from app.catalog import blueprint
from app.catalog.models import (
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
    Theme,
)
from app.extensions import db


@blueprint.cli.command("create-db")
@with_appcontext
def createdb():
    db.create_all()


def _donwload_gzip_file(url: str, dest: str):
    response = requests.get(url, stream=True)
    with open(dest, "wb") as dest_fp:
        with gzip.open(response.raw, "rb") as data:
            dest_fp.write(data.read())


def _get_files_dest(directory: str, url: str):
    return os.path.join(directory, os.path.splitext(os.path.basename(url))[0])


@contextlib.contextmanager
def _read_csv(filename: str):
    with open(filename, encoding="utf-8") as fp:
        reader = csv.reader(fp)
        next(reader)

        yield reader


Model_T = TypeVar("Model_T")
ProcessRow_Return_T = TypeVar("ProcessRow_Return_T")


def _get_importer(
    _cls: Type[Model_T],
    process_row: Callable[[Iterator[List[str]]], ProcessRow_Return_T],
    after_process: Callable[
        [ProcessRow_Return_T], Generator[Model_T, None, None]
    ] = None,
):
    def _importer(filename: str):
        with _read_csv(filename) as reader:
            _rows = map(process_row, reader)
            if callable(after_process):
                _rows = after_process(_rows)

            db.session.add_all(_rows)
            db.session.commit()

    return _importer


_import_themes = _get_importer(
    Theme,
    lambda row: Theme(
        id=int(row[0]),
        name=row[1],
        parent_id=int(row[2]) if row[2].isnumeric() else None,
    ),
)

_import_colors = _get_importer(
    Color,
    lambda row: Color(
        id=int(row[0]), name=row[1], rgb=row[2], is_trans=(row[3] == "t")
    ),
)

_import_part_categories = _get_importer(
    PartsCategory,
    lambda row: PartsCategory(
        id=int(row[0]),
        name=row[1],
    ),
)

_import_parts = _get_importer(
    Part,
    lambda row: Part(
        part_num=row[0],
        name=row[1],
        part_material=row[3],
        part_category_id=int(row[2]),
    ),
)

_import_part_relationships = _get_importer(
    PartsRelationship,
    lambda row: PartsRelationship(
        rel_type=row[0], child_part_id=row[1], parent_part_id=row[2]
    ),
)

_import_elements = _get_importer(
    Element,
    lambda row: Element(
        element_id=int(row[0]), part_id=row[1], color_id=int(row[2])
    ),
)

_import_minifigs = _get_importer(
    Minifig,
    lambda row: Minifig(
        fig_num=row[0], name=row[1], num_parts=int(row[2]), img_url=row[3]
    ),
)

_import_sets = _get_importer(
    Set,
    lambda row: Set(
        set_num=row[0],
        name=row[1],
        year=int(row[2]),
        theme_id=int(row[3]),
        num_parts=int(row[4]),
        img_url=row[5],
    ),
)

_import_inventories = _get_importer(
    Inventory,
    lambda row: Inventory(
        id=int(row[0]),
        version=int(row[1]),
        is_minifig=row[2].startswith("fig-"),
        set_id=row[2] if not row[2].startswith("fig-") else None,
        minifig_id=row[2] if row[2].startswith("fig-") else None,
    ),
)

_import_inventory_minifigs = _get_importer(
    InventoryMinifigs,
    lambda row: InventoryMinifigs(
        inventory_id=int(row[0]), minifig_id=row[1], quantity=int(row[2])
    ),
)

_import_inventory_parts = _get_importer(
    InventoryParts,
    lambda row: InventoryParts(
        inventory_id=int(row[0]),
        part_id=row[1],
        color_id=int(row[2]),
        quantity=int(row[3]),
        is_spare=row[4] == "t",
        img_url=row[5],
    ),
)

_import_inventory_sets = _get_importer(
    InventorySets,
    lambda row: InventorySets(
        inventory_id=int(row[0]), set_id=row[1], quantity=int(row[2])
    ),
)

_DATA_URLS = [
    (
        "https://cdn.rebrickable.com/media/downloads/themes.csv.gz",
        _import_themes,
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/colors.csv.gz",
        _import_colors,
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/part_categories.csv.gz",
        _import_part_categories,
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/parts.csv.gz",
        _import_parts,
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/part_relationships.csv.gz",
        _import_part_relationships,
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/elements.csv.gz",
        _import_elements,
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/minifigs.csv.gz",
        _import_minifigs,
    ),
    ("https://cdn.rebrickable.com/media/downloads/sets.csv.gz", _import_sets),
    (
        "https://cdn.rebrickable.com/media/downloads/inventories.csv.gz",
        _import_inventories,
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/inventory_minifigs.csv.gz",
        _import_inventory_minifigs,
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/inventory_parts.csv.gz",
        _import_inventory_parts,
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/inventory_sets.csv.gz",
        _import_inventory_sets,
    ),
]


@blueprint.cli.command("load")
@with_appcontext
def load_data():
    db.drop_all()
    db.create_all()

    directory = ""
    try:
        directory = tempfile.mkdtemp()

        for url, _import in _DATA_URLS:
            filename = _get_files_dest(directory, url)
            _donwload_gzip_file(url, filename)
            print("Downloaded file {} ({})".format(filename, url))

            print("Importing data from {}".format(filename))
            _import(filename)
    finally:
        if os.path.exists(directory):
            shutil.rmtree(directory)
