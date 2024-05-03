"""
Import data from rebrickable

1. Download all files in temp directory
2. Import colors and themes
3. Import years and then sets and minifigs
4. Import parts and part categories
5. Import elements
6. Import parts from sets
"""
import gzip
import os
import shutil
import tempfile

import numpy as np
import pandas as pd
import requests
import sqlalchemy as sa
from celery import shared_task

from app.extensions import db
from app.models.orm.lego import (
    Color,
    Element,
    GenericSet,
    GenericSetPart,
    GenericSetRelationship,
    Part,
    PartCategory,
    Theme,
    Year,
)

_URLS = {
    "themes": "https://cdn.rebrickable.com/media/downloads/themes.csv.gz",
    "colors": "https://cdn.rebrickable.com/media/downloads/colors.csv.gz",
    "part_categories": "https://cdn.rebrickable.com/media/downloads/part_categories.csv.gz",
    "parts": "https://cdn.rebrickable.com/media/downloads/parts.csv.gz",
    "part_relationships": "https://cdn.rebrickable.com/media/downloads/part_relationships.csv.gz",
    "elements": "https://cdn.rebrickable.com/media/downloads/elements.csv.gz",
    "minifigs": "https://cdn.rebrickable.com/media/downloads/minifigs.csv.gz",
    "sets": "https://cdn.rebrickable.com/media/downloads/sets.csv.gz",
    "inventories": "https://cdn.rebrickable.com/media/downloads/inventories.csv.gz",
    "inventory_minifigs": "https://cdn.rebrickable.com/media/downloads/inventory_minifigs.csv.gz",
    "inventory_parts": "https://cdn.rebrickable.com/media/downloads/inventory_parts.csv.gz",
    "inventory_sets": "https://cdn.rebrickable.com/media/downloads/inventory_sets.csv.gz",
}


def _download_gzip_file(url: str, dest: str):
    response = requests.get(url, stream=True, timeout=10)
    with open(dest, "wb") as dest_fp, gzip.open(response.raw, "rb") as data:
        buffer = data.read()
        if isinstance(buffer, str):
            dest_fp.write(buffer.encode())
        else:
            dest_fp.write(buffer)


def _get_files_dest(directory: str, url: str):
    return os.path.join(directory, os.path.splitext(os.path.basename(url))[0])


def _download_files(directory: str):
    for url in _URLS.values():
        filename = _get_files_dest(directory, url)
        _download_gzip_file(url, filename)
        print(f"Downloaded file {filename} ({url})")


# Imports Basic Models
def import_colors(directory: str):
    filename = _get_files_dest(directory, _URLS["colors"])

    def _build_color(row):
        curr = db.session.get(Color, int(row.id))
        if curr is None:
            curr = Color(
                id=int(row.id),
                name=str(row.name),
                rgb=str(row.rgb),
                is_trans=row.is_trans == "t",
            )
        else:
            curr.name = str(row.name)
            curr.rgb = str(row.rgb)
            curr.is_trans = row.is_trans == "t"

        return curr

    color_df = pd.read_csv(filename)
    colors = map(_build_color, color_df.itertuples())
    db.session.add_all(colors)
    db.session.flush()

    print("Colors Imported")


def import_themes(directory: str):
    filename = _get_files_dest(directory, _URLS["themes"])

    def _build_theme(row):
        curr = db.session.get(Theme, int(row.id))
        parent_id = int(row.parent_id) if row.parent_id is not None else None

        if curr is None:
            curr = Theme(id=int(row.id), name=str(row.name), parent_id=parent_id)
        else:
            curr.name = str(row.name)
            curr.parent_id = parent_id

        return curr

    themes_df = pd.read_csv(filename)
    themes_df.replace(np.nan, None, inplace=True)
    themes = map(_build_theme, themes_df.itertuples())
    db.session.add_all(themes)
    db.session.flush()

    print("Themes Imported")


def import_sets(directory: str):
    filename = _get_files_dest(directory, _URLS["sets"])

    def _build_year(value):
        curr = db.session.get(Year, value)
        if curr is None:
            curr = Year(id=value, name=str(value))
        return curr

    def _build_set(row):
        curr = db.session.get(GenericSet, str(row.set_num))
        theme = db.session.get(Theme, int(row.theme_id))
        year = db.session.get(Year, int(row.year))
        if year is None or theme is None:
            return None

        if curr is None:
            curr = GenericSet(
                id=str(row.set_num),
                name=str(row.name),
                num_parts=int(row.num_parts),
                img_url=str(row.img_url),
                is_minifig=False,
                theme=theme,
                year=year,
            )
        else:
            curr.name = str(row.name)
            curr.num_parts = int(row.num_parts)
            curr.img_url = str(row.img_url)
            curr.is_minifig = False
            curr.theme = theme
            curr.year = year

        return curr

    set_df = pd.read_csv(filename)

    years = [
        _build_year(item[1])
        for item in set_df["year"].astype(np.int64).drop_duplicates().items()
    ]
    db.session.add_all(years)
    db.session.flush()

    sets = [
        item
        for item in [_build_set(item) for item in set_df.itertuples()]
        if item is not None
    ]
    db.session.add_all(sets)
    db.session.flush()

    print("Sets Imported")


def import_minifigs(directory: str):
    filename = _get_files_dest(directory, _URLS["minifigs"])

    def _build_fig(row):
        curr = db.session.get(GenericSet, str(row.fig_num))
        if curr is None:
            curr = GenericSet(
                id=str(row.fig_num),
                name=str(row.name),
                num_parts=int(row.num_parts),
                img_url=str(row.img_url),
                is_minifig=True,
                theme_id=None,
                year_id=None,
            )
        else:
            curr.name = str(row.name)
            curr.num_parts = int(row.num_parts)
            curr.img_url = str(row.img_url)
            curr.is_minifig = True
            curr.theme_id = None
            curr.year_id = None

        return curr

    minifig_df = pd.read_csv(filename)
    minifigs = map(_build_fig, minifig_df.itertuples())
    db.session.add_all(minifigs)
    db.session.flush()

    print("Minifigs Imported")


def import_parts(directory: str):
    parts_filename = _get_files_dest(directory, _URLS["parts"])
    categories_filename = _get_files_dest(directory, _URLS["part_categories"])

    def _build_category(row):
        curr = db.session.get(PartCategory, int(row.id))
        if curr is None:
            curr = PartCategory(id=int(row.id), name=str(row.name))
        else:
            curr.name = str(row.name)

        return curr

    def _build_part(row):
        curr = db.session.get(Part, str(row.part_num))
        category = db.session.get(PartCategory, int(row.part_cat_id))
        if category is None:
            return None

        if curr is None:
            curr = Part(
                id=str(row.part_num),
                name=str(row.name),
                material=str(row.part_material),
                category=category,
            )
        else:
            curr.name = str(row.name)
            curr.material = str(row.part_material)
            curr.category = category

        return curr

    categories_df = pd.read_csv(categories_filename)
    categories = map(_build_category, categories_df.itertuples())
    db.session.add_all(categories)
    db.session.flush()

    parts_df = pd.read_csv(parts_filename)
    parts = [
        item for item in map(_build_part, parts_df.itertuples()) if item is not None
    ]
    db.session.add_all(parts)
    db.session.flush()

    print("Parts Imported")


def import_elements(directory: str):
    filename = _get_files_dest(directory, _URLS["elements"])

    def _build_element(row):
        curr = db.session.get(Element, int(row.element_id))
        part = db.session.get(Part, str(row.part_num))
        color = db.session.get(Color, int(row.color_id))
        if part is None or color is None:
            return None

        if curr is None:
            curr = Element(
                id=int(row.element_id),
                part=part,
                color=color,
                # design_id=str(row.design_id) # TODO: Add column in model
            )
        else:
            curr.part = part
            curr.color = color

        return curr

    elements_df = pd.read_csv(filename)
    elements = [
        item
        for item in map(_build_element, elements_df.itertuples())
        if item is not None
    ]
    db.session.add_all(elements)
    db.session.flush()

    print("Elements Imported")


# Import Relationships
def import_relationships(directory: str):
    db.session.execute(sa.delete(GenericSetRelationship))
    db.session.execute(sa.delete(GenericSetPart))

    def _build_set_rel(row):
        parent = db.session.get(GenericSet, str(row.set_num_parent))
        child = db.session.get(GenericSet, str(row.set_num_child))
        if parent is None or child is None:
            return None

        return GenericSetRelationship(
            parent=parent,
            child=child,
            quantity=int(row.quantity),
        )

    def _build_part_rel(row):
        _set = db.session.get(GenericSet, str(row.set_num))
        part = db.session.get(Part, str(row.part_num))
        color = db.session.get(Color, int(row.color_id))

        return GenericSetPart(
            set=_set,
            part=part,
            color=color,
            quantity=int(row.quantity),
            is_spare=row.is_spare == "t",
            img_url=str(row.img_url),
        )

    inventory_df = pd.read_csv(_get_files_dest(directory, _URLS["inventories"]))
    inventory_df.sort_values(["version", "set_num"], inplace=True)
    inventory_df.drop_duplicates(["set_num"], inplace=True, keep="last")

    # Import sets relationships
    inventory_sets_df = pd.read_csv(_get_files_dest(directory, _URLS["inventory_sets"]))
    inventory_sets_rels_df = pd.merge(
        inventory_df,
        inventory_sets_df,
        how="inner",
        left_on="id",
        right_on="inventory_id",
        suffixes=("_parent", "_child"),
    )
    inventory_sets = [
        item
        for item in map(_build_set_rel, inventory_sets_rels_df.itertuples())
        if item is not None
    ]
    db.session.add_all(inventory_sets)
    db.session.flush()

    # Import minifigs relationships
    inventory_minifigs_df = pd.read_csv(
        _get_files_dest(directory, _URLS["inventory_minifigs"])
    )
    inventory_minifigs_rels_df = pd.merge(
        inventory_df,
        inventory_minifigs_df.rename(columns={"fig_num": "set_num"}),
        how="inner",
        left_on="id",
        right_on="inventory_id",
        suffixes=("_parent", "_child"),
    )
    inventory_minifigs = [
        item
        for item in map(_build_set_rel, inventory_minifigs_rels_df.itertuples())
        if item is not None
    ]
    db.session.add_all(inventory_minifigs)
    db.session.flush()

    # Import parts relationships
    inventory_parts_df = pd.read_csv(
        _get_files_dest(directory, _URLS["inventory_parts"])
    )
    inventory_parts_rels_df = pd.merge(
        inventory_df,
        inventory_parts_df,
        how="inner",
        left_on="id",
        right_on="inventory_id",
        suffixes=("_parent", "_child"),
    )
    inventory_parts = [
        item
        for item in map(_build_part_rel, inventory_parts_rels_df.itertuples())
        if item is not None
    ]
    db.session.add_all(inventory_parts)
    db.session.flush()

    print("Relationships Imported")


@shared_task
def import_data():
    directory = ""
    try:
        directory = tempfile.mkdtemp()
        _download_files(directory)

        with db.session.no_autoflush:
            import_colors(directory)
            import_themes(directory)
            import_sets(directory)
            import_minifigs(directory)
            import_parts(directory)
            import_elements(directory)
            import_relationships(directory)
            db.session.commit()
    finally:
        if os.path.exists(directory):
            shutil.rmtree(directory)
