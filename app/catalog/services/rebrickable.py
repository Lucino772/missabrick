import abc
import csv
import gzip
import os

import requests

from app.catalog.services.colors import SqlColorsService
from app.catalog.services.elements import SqlElementsService
from app.catalog.services.inventories import SqlInventoriesService
from app.catalog.services.inventory_minifigs import SqlInventoryMinifigsService
from app.catalog.services.inventory_parts import SqlInventoryPartsService
from app.catalog.services.inventory_sets import SqlInventorySetsService
from app.catalog.services.minifigs import SqlMinifigsService
from app.catalog.services.part_categories import SqlPartsCategoriesService
from app.catalog.services.part_relationships import (
    SqlPartsRelationshipsService,
)
from app.catalog.services.parts import SqlPartsService
from app.catalog.services.sets import SqlSetsService
from app.catalog.services.themes import SqlThemesService


class AbstractRebrickableService(abc.ABC):
    @abc.abstractmethod
    def imports(self, directory: str):
        raise NotImplementedError


class RebrickableService(AbstractRebrickableService):
    def __init__(
        self,
        colors_srv: SqlColorsService,
        elements_srv: SqlElementsService,
        inv_minifigs_srv: SqlInventoryMinifigsService,
        inv_parts_srv: SqlInventoryPartsService,
        inv_sets_srv: SqlInventorySetsService,
        inventories_srv: SqlInventoriesService,
        minifigs_srv: SqlMinifigsService,
        parts_cats_srv: SqlPartsCategoriesService,
        parts_rels_srv: SqlPartsRelationshipsService,
        parts_srv: SqlPartsService,
        sets_srv: SqlSetsService,
        themes_srv: SqlThemesService,
    ):
        self.__imports = [
            (
                "https://cdn.rebrickable.com/media/downloads/themes.csv.gz",
                themes_srv,
                ["id", "name", "parent_id"],
            ),
            (
                "https://cdn.rebrickable.com/media/downloads/colors.csv.gz",
                colors_srv,
                ["id", "name", "rgb", "is_trans"],
            ),
            (
                "https://cdn.rebrickable.com/media/downloads/part_categories.csv.gz",
                parts_cats_srv,
                ["id", "name"],
            ),
            (
                "https://cdn.rebrickable.com/media/downloads/parts.csv.gz",
                parts_srv,
                ["part_num", "name", "part_cat_id", "part_material"],
            ),
            (
                "https://cdn.rebrickable.com/media/downloads/part_relationships.csv.gz",
                parts_rels_srv,
                ["rel_type", "child_part_num", "parent_part_num"],
            ),
            (
                "https://cdn.rebrickable.com/media/downloads/elements.csv.gz",
                elements_srv,
                ["element_id", "part_num", "color_id"],
            ),
            (
                "https://cdn.rebrickable.com/media/downloads/minifigs.csv.gz",
                minifigs_srv,
                ["fig_num", "name", "num_parts", "img_url"],
            ),
            (
                "https://cdn.rebrickable.com/media/downloads/sets.csv.gz",
                sets_srv,
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
                inventories_srv,
                ["id", "version", "set_num"],
            ),
            (
                "https://cdn.rebrickable.com/media/downloads/inventory_minifigs.csv.gz",
                inv_minifigs_srv,
                ["inventory_id", "fig_num", "quantity"],
            ),
            (
                "https://cdn.rebrickable.com/media/downloads/inventory_parts.csv.gz",
                inv_parts_srv,
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
                inv_sets_srv,
                ["inventory_id", "set_num", "quantity"],
            ),
        ]

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
    def _import(filename, _import, fields: list):
        with open(filename, encoding="utf-8") as fp:
            reader = csv.DictReader(fp, fieldnames=fields)
            next(reader)

            _import(reader)

    def imports(self, directory: str):
        for url, srv, fields in self.__imports:
            filename = self._get_files_dest(directory, url)
            self._download_gzip_file(url, filename)
            print("Downloaded file {} ({})".format(filename, url))

            print("Importing data from {}".format(filename))
            self._import(filename, srv.imports, fields)
