import typing as t

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class Theme(db.Model):
    __tablename__ = "theme"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    parent_id: Mapped[int] = mapped_column(sa.ForeignKey("theme.id"))

    parent: Mapped["Theme"] = relationship()
    childs: Mapped[t.List["Theme"]] = relationship()

class Color(db.Model):
    __tablename__ = "color"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    rgb: Mapped[str] = mapped_column(sa.String(20))
    is_trans: Mapped[bool] = mapped_column()

class PartsCategory(db.Model):
    __tablename__ = "parts_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))

class Part(db.Model):
    __tablename__ = "part"

    part_num: Mapped[str] = mapped_column(sa.String(20), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    part_material: Mapped[str] = mapped_column(sa.String(255))
    part_category_id: Mapped[int] = mapped_column(sa.ForeignKey("parts_category.id"))

    part_category: Mapped[PartsCategory] = relationship()

class PartsRelationship(db.Model):
    __tablename__ = "parts_relationship"

    id: Mapped[int] = mapped_column(primary_key=True)
    rel_type: Mapped[str] = mapped_column(sa.String(10))
    child_part_id: Mapped[str] = mapped_column(sa.ForeignKey("part.part_num"))
    parent_part_id: Mapped[str] = mapped_column(sa.ForeignKey("part.part_num"))

    child_part: Mapped[Part] = relationship()
    parent_part: Mapped[Part] = relationship()

class Element(db.Model):
    __tablename__ = "element"

    element_id: Mapped[int] = mapped_column(primary_key=True)
    color_id: Mapped[int] = mapped_column(sa.ForeignKey("color.id"))
    part_id: Mapped[str] = mapped_column(sa.ForeignKey("part.part_num"))

    color: Mapped[Color] = relationship()
    part: Mapped[Part] = relationship()

class Minifig(db.Model):
    __tablename__ = "minifig"

    fig_num: Mapped[str] = mapped_column(sa.String(20), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    num_parts: Mapped[int] = mapped_column()
    img_url: Mapped[str] = mapped_column(sa.Text)

class Set(db.Model):
    __tablename__ = "set"

    set_num: Mapped[str] = mapped_column(sa.String(20), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    year: Mapped[int] = mapped_column()
    num_parts: Mapped[int] = mapped_column()
    img_url: Mapped[str] = mapped_column(sa.Text)
    theme_id: Mapped[int] = mapped_column(sa.ForeignKey("theme.id"))

    theme: Mapped[Theme] = relationship()

class Inventory(db.Model):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    version: Mapped[int] = mapped_column()
    is_minifig: Mapped[bool] = mapped_column()
    set_id: Mapped[str] = mapped_column(sa.ForeignKey("set.set_num"))
    minifig_id: Mapped[str] = mapped_column(sa.ForeignKey("minifig.fig_num"))

    _set: Mapped[Set] = relationship()
    minifig: Mapped[Minifig] = relationship()

class InventoryMinifigs(db.Model):
    __tablename__ = "inventory_minifigs"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column()
    inventory_id: Mapped[int] = mapped_column(sa.ForeignKey("inventory.id"))
    minifig_id: Mapped[str] = mapped_column(sa.ForeignKey("minifig.fig_num"))

    inventory: Mapped[Inventory] = relationship()
    minifig: Mapped[Minifig] = relationship()

class InventoryParts(db.Model):
    __tablename__ = "inventory_parts"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column()
    is_spare: Mapped[bool] = mapped_column()
    img_url: Mapped[str] = mapped_column(sa.Text)
    inventory_id: Mapped[int] = mapped_column(sa.ForeignKey("inventory.id"))
    part_id: Mapped[str] = mapped_column(sa.String, sa.ForeignKey("part.part_num"))
    color_id: Mapped[int] = mapped_column(sa.ForeignKey("color.id"))

    inventory: Mapped[Inventory] = relationship()
    part: Mapped[Part] = relationship()
    color: Mapped[Color] = relationship()

class InventorySets(db.Model):
    __tablename__ = "inventory_sets"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column()
    inventory_id: Mapped[int] = mapped_column(sa.ForeignKey("inventory.id"))
    set_id: Mapped[str] = mapped_column(sa.String, sa.ForeignKey("set.set_num"))

    inventory: Mapped[Inventory] = db.relationship()
    _set: Mapped[Set] = db.relationship()
