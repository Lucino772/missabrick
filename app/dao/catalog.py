import sqlalchemy as sa

from app.dao._generic import GenericDao
from app.errors import SetDoesNotExists
from app.models.catalog import (
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


class ColorDao(GenericDao[Color]):
    def imports(self, data: list):
        self.session.execute(sa.delete(Color))
        items = map(
            lambda item: Color(
                id=int(item["id"]),
                name=item["name"],
                rgb=item["rgb"],
                is_trans=(item["is_trans"] == "t"),
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()


class ElementDao(GenericDao[Element]):
    def imports(self, data: list):
        self.session.execute(sa.delete(Element))
        items = map(
            lambda item: Element(
                element_id=int(item["element_id"]),
                part_id=item["part_num"],
                color_id=int(item["color_id"]),
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()


class ThemeDao(GenericDao[Theme]):
    def imports(self, data: list):
        self.session.execute(sa.delete(Theme))

        def _to_model(item: dict):
            if item["parent_id"].isnumeric():
                parent_id = int(item["parent_id"])
            else:
                parent_id = None

            return Theme(
                id=int(item["id"]),
                name=item["name"],
                parent_id=parent_id,
            )

        items = map(_to_model, data)
        self.session.add_all(items)
        self.session.commit()


class InventorySetDao(GenericDao[InventorySets]):
    def imports(self, data: list):
        self.session.execute(sa.delete(InventorySets))
        items = map(
            lambda item: InventorySets(
                inventory_id=int(item["inventory_id"]),
                set_id=item["set_num"],
                quantity=int(item["quantity"]),
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()


class InventoryPartDao(GenericDao[InventoryParts]):
    def imports(self, data: list):
        self.session.execute(sa.delete(InventoryParts))
        items = map(
            lambda item: InventoryParts(
                inventory_id=int(item["inventory_id"]),
                part_id=item["part_num"],
                color_id=int(item["color_id"]),
                quantity=int(item["quantity"]),
                is_spare=item["is_spare"] == "t",
                img_url=item["img_url"],
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()

    def format_elements(self, inv_part: InventoryParts):
        results = (
            self.session.execute(
                inv_part.part.elements.filter_by(color=inv_part.color)
            )
            .scalars()
            .all()
        )

        if len(results) == 0:
            yield {
                "part_num": inv_part.part.part_num,
                "color_id": inv_part.color.id,
                "element_id": None,
            }
        else:
            for elem in results:
                yield {
                    "part_num": inv_part.part.part_num,
                    "color_id": inv_part.color.id,
                    "element_id": elem.element_id,
                }


class InventoryMinifigDao(GenericDao[InventoryMinifigs]):
    def imports(self, data: list):
        self.session.execute(sa.delete(InventoryMinifigs))
        items = map(
            lambda item: InventoryMinifigs(
                inventory_id=int(item["inventory_id"]),
                minifig_id=item["fig_num"],
                quantity=int(item["quantity"]),
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()

    def get_parts(self, inv_fig: InventoryMinifigs):
        return (
            self.session.execute(
                inv_fig.minifig.inventories.order_by(Inventory.version)
            )
            .scalars()
            .first()
            .inventory_parts
        )


class InventoryDao(GenericDao[Inventory]):
    def imports(self, data: list):
        self.session.execute(sa.delete(Inventory))

        def _to_model(item: dict):
            is_minifig = item["set_num"].startswith("fig-")
            if is_minifig:
                set_id = None
                minifig_id = item["set_num"]
            else:
                set_id = item["set_num"]
                minifig_id = None

            return Inventory(
                id=int(item["id"]),
                version=int(item["version"]),
                is_minifig=is_minifig,
                set_id=set_id,
                minifig_id=minifig_id,
            )

        items = map(_to_model, data)
        self.session.add_all(items)
        self.session.commit()

    def get_inventories(
        self, set_id: str, quantity: int = 1, recursive: bool = True
    ):
        inventory = (
            self.session.execute(
                sa.select(Inventory)
                .filter(Inventory.set_id == set_id)
                .order_by(Inventory.version)
            )
            .scalars()
            .first()
        )
        if inventory is None:
            return  # TODO: Raise Exception

        inventories = [(inventory, quantity)]

        if recursive:
            for inv_set in inventory.inventory_sets:
                inventories += self.get_inventories(
                    inv_set.set_id, inv_set.quantity * quantity, recursive=True
                )

        return inventories


class MinifigDao(GenericDao[Minifig]):
    def imports(self, data: list):
        self.session.execute(sa.delete(Minifig))
        items = map(
            lambda item: Minifig(
                fig_num=item["fig_num"],
                name=item["name"],
                num_parts=int(item["num_parts"]),
                img_url=item["img_url"],
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()


class SetDao(GenericDao[Set]):
    def imports(self, data: list):
        self.session.execute(sa.delete(Set))
        items = map(
            lambda item: Set(
                set_num=item["set_num"],
                name=item["name"],
                year=int(item["year"]),
                theme_id=int(item["theme_id"]),
                num_parts=int(item["num_parts"]),
                img_url=item["img_url"],
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()

    def search(
        self,
        filters: list,
        search: str,
        paginate: bool = False,
        current_page: int = None,
        page_size: int = None,
    ):
        select = sa.select(Set).order_by(Set.year)

        if len(search) > 0:
            select = select.filter(
                sa.or_(
                    Set.set_num.contains(search),
                    Set.name.contains(search),
                )
            )

        for key, value in filters:
            if key == "theme":
                theme_id = (
                    self.session.execute(
                        sa.select(Theme.id).filter(
                            Theme.name.contains(str(value))
                        )
                    )
                    .scalars()
                    .all()
                )
                if len(theme_id) > 0:
                    select = select.filter(Set.theme_id.in_(theme_id))
            elif key == "year":
                select = select.filter(Set.year == int(value))
            elif key == "name":
                select = select.filter(Set.name.contains(str(value)))
            elif key == "id":
                select = select.filter(Set.set_num.contains(str(value)))

        if paginate:
            return self.db.paginate(
                select, page=current_page, per_page=page_size
            )
        else:
            return self.session.execute(select).scalars().all()

    def get_years(self):
        return (
            self.session.execute(
                sa.select(Set.year).distinct().order_by(Set.year)
            )
            .scalars()
            .all()
        )

    def get_inventories(
        self, set_num: str, quantity: int = 1, recursive: bool = True
    ):
        aset = (
            self.session.execute(sa.select(Set).filter(Set.set_num == set_num))
            .scalars()
            .first()
        )
        if aset is None:
            raise SetDoesNotExists()

        inventory = (
            self.session.execute(
                sa.select(Inventory)
                .filter(Inventory.set_id == aset.set_num)
                .order_by(Inventory.version)
            )
            .scalars()
            .first()
        )
        if inventory is None:
            raise SetDoesNotExists()

        inventories = [(inventory, quantity)]

        if recursive is True:
            for inv_set in inventory.inventory_sets:
                inventories += self.get_inventories(
                    inv_set.set_id, inv_set.quantity * quantity, recursive=True
                )

        return inventories


class PartDao(GenericDao[Part]):
    def imports(self, data: list):
        self.session.execute(sa.delete(Part))
        items = map(
            lambda item: Part(
                part_num=item["part_num"],
                name=item["name"],
                part_material=item["part_material"],
                part_category_id=int(item["part_cat_id"]),
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()


class PartRelationshipDao(GenericDao[PartsRelationship]):
    def imports(self, data: list):
        self.session.execute(sa.delete(PartsRelationship))
        items = map(
            lambda item: PartsRelationship(
                rel_type=item["rel_type"],
                child_part_id=item["child_part_num"],
                parent_part_id=item["parent_part_num"],
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()


class PartCategoryDao(GenericDao[PartsCategory]):
    def imports(self, data: list):
        self.session.execute(sa.delete(PartsCategory))
        items = map(
            lambda item: PartsCategory(
                id=int(item["id"]),
                name=item["name"],
            ),
            data,
        )
        self.session.add_all(items)
        self.session.commit()


part_category_dao = PartCategoryDao(PartsCategory)
part_relationship_dao = PartRelationshipDao(PartsRelationship)
part_dao = PartDao(Part)
set_dao = SetDao(Set)
inventory_dao = InventoryDao(Inventory)
inv_minifig_dao = InventoryMinifigDao(InventoryMinifigs)
inv_set_dao = InventorySetDao(InventorySets)
theme_dao = ThemeDao(Theme)
element_dao = ElementDao(Element)
color_dao = ColorDao(Color)
minifig_dao = MinifigDao(Minifig)
inv_part_dao = InventoryPartDao(InventoryParts)
