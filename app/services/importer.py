import csv
import gzip
import os
import typing as t

import requests

from app.dao.catalog import (
    color_dao,
    element_dao,
    inv_minifig_dao,
    inv_part_dao,
    inv_set_dao,
    inventory_dao,
    minifig_dao,
    part_category_dao,
    part_dao,
    part_relationship_dao,
    set_dao,
    theme_dao,
)

_IMPORTS: t.List[
    t.Tuple[str, t.Callable[[t.Iterable], t.NoReturn], t.List[str]]
] = [
    (
        "https://cdn.rebrickable.com/media/downloads/themes.csv.gz",
        theme_dao.imports,
        ["id", "name", "parent_id"],
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/colors.csv.gz",
        color_dao.imports,
        ["id", "name", "rgb", "is_trans"],
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/part_categories.csv.gz",
        part_category_dao.imports,
        ["id", "name"],
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/parts.csv.gz",
        part_dao.imports,
        ["part_num", "name", "part_cat_id", "part_material"],
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/part_relationships.csv.gz",
        part_relationship_dao.imports,
        ["rel_type", "child_part_num", "parent_part_num"],
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/elements.csv.gz",
        element_dao.imports,
        ["element_id", "part_num", "color_id"],
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/minifigs.csv.gz",
        minifig_dao.imports,
        ["fig_num", "name", "num_parts", "img_url"],
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/sets.csv.gz",
        set_dao.imports,
        [
            "set_num",
            "name",
            "year",
            "theme_id",
            "num_parts",
            "img_url",
        ],
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/inventories.csv.gz",
        inventory_dao.imports,
        ["id", "version", "set_num"],
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/inventory_minifigs.csv.gz",
        inv_minifig_dao.imports,
        ["inventory_id", "fig_num", "quantity"],
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/inventory_parts.csv.gz",
        inv_part_dao.imports,
        [
            "inventory_id",
            "part_num",
            "color_id",
            "quantity",
            "is_spare",
            "img_url",
        ],
    ),
    (
        "https://cdn.rebrickable.com/media/downloads/inventory_sets.csv.gz",
        inv_set_dao.imports,
        ["inventory_id", "set_num", "quantity"],
    ),
]


class ImporterService:
    @staticmethod
    def _download_gzip_file(url: str, dest: str):
        response = requests.get(url, stream=True)
        with open(dest, "wb") as dest_fp:
            with gzip.open(response.raw, "rb") as data:
                dest_fp.write(data.read())

    @staticmethod
    def _get_files_dest(directory: str, url: str):
        return os.path.join(
            directory, os.path.splitext(os.path.basename(url))[0]
        )

    @staticmethod
    def _import(
        filename, _import: t.Callable[[t.Iterable], t.NoReturn], fields: list
    ):
        with open(filename, encoding="utf-8") as fp:
            reader = csv.DictReader(fp, fieldnames=fields)
            next(reader)

            _import(reader)

    def imports(self, directory: str):
        for url, imports, fields in _IMPORTS:
            filename = self._get_files_dest(directory, url)
            self._download_gzip_file(url, filename)
            print("Downloaded file {} ({})".format(filename, url))

            print("Importing data from {}".format(filename))
            self._import(filename, imports, fields)


importer_service = ImporterService()
