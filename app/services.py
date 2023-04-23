from app.catalog.services import (
    RebrickableService,
    ReportService,
    SqlColorsService,
    SqlElementsService,
    SqlInventoriesService,
    SqlInventoryMinifigsService,
    SqlInventoryPartsService,
    SqlInventorySetsService,
    SqlMinifigsService,
    SqlPartsCategoriesService,
    SqlPartsRelationshipsService,
    SqlPartsService,
    SqlSetsService,
    SqlThemesService,
)

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
