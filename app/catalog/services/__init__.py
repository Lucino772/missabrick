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
from app.catalog.services.rebrickable import RebrickableService
from app.catalog.services.report import ReportService
from app.catalog.services.sets import SqlSetsService
from app.catalog.services.themes import SqlThemesService

colors_srv = SqlColorsService()
elements_srv = SqlElementsService()
inventories_srv = SqlInventoriesService()
inv_minifigs_srv = SqlInventoryMinifigsService()
inv_parts_srv = SqlInventoryPartsService()
inv_sets_srv = SqlInventorySetsService()
minifigs_srv = SqlMinifigsService()
parts_rels_srv = SqlPartsRelationshipsService()
parts_cats_srv = SqlPartsCategoriesService()
parts_srv = SqlPartsService()
sets_srv = SqlSetsService()
themes_srv = SqlThemesService()

rebrickable_srv = RebrickableService(
    colors_srv=colors_srv,
    elements_srv=elements_srv,
    inventories_srv=inventories_srv,
    inv_minifigs_srv=inv_minifigs_srv,
    inv_parts_srv=inv_parts_srv,
    inv_sets_srv=inv_sets_srv,
    minifigs_srv=minifigs_srv,
    parts_rels_srv=parts_rels_srv,
    parts_cats_srv=parts_cats_srv,
    parts_srv=parts_srv,
    sets_srv=sets_srv,
    themes_srv=themes_srv,
)

report_srv = ReportService()
