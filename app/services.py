from app.catalog.services import (
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
