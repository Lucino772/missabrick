import typing as t

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


# Theme, Year & Color
class Theme(db.Model):
    __tablename__ = "theme"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))

    # Theme
    parent_id: Mapped[t.Optional[int]] = mapped_column(
        sa.ForeignKey("theme.id")
    )
    parent: Mapped[t.Optional["Theme"]] = relationship()

    # GenericSet
    sets: Mapped[t.List["GenericSet"]] = relationship(back_populates="theme")


class Year(db.Model):
    __tablename__ = "year"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(sa.Integer())

    # GenericSet
    sets: Mapped[t.List["GenericSet"]] = relationship(back_populates="year")


class Color(db.Model):
    __tablename__ = "color"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    rgb: Mapped[str] = mapped_column(sa.String(20))
    is_trans: Mapped[bool] = mapped_column()

    # GenericSetPart
    parts: Mapped[t.List["GenericSetPart"]] = relationship(
        back_populates="color"
    )

    # Element
    elements: Mapped[t.List["Element"]] = relationship(back_populates="color")


# Sets (Set & Minifig)
class GenericSetRelationship(db.Model):
    __tablename__ = "generic_set_rel"

    quantity: Mapped[int] = mapped_column()

    # GenericSet (Parent)
    parent_id: Mapped[str] = mapped_column(
        sa.String, sa.ForeignKey("generic_set.id"), primary_key=True
    )
    parent: Mapped["GenericSet"] = relationship(foreign_keys=[parent_id])

    # GenericSet (Child)
    child_id: Mapped[str] = mapped_column(
        sa.String, sa.ForeignKey("generic_set.id"), primary_key=True
    )
    child: Mapped["GenericSet"] = relationship(foreign_keys=[child_id])


class GenericSet(db.Model):
    __tablename__ = "generic_set"

    id: Mapped[str] = mapped_column(sa.String(20), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    num_parts: Mapped[int] = mapped_column()
    img_url: Mapped[str] = mapped_column(sa.Text)
    is_minifig: Mapped[bool] = mapped_column()

    # Theme
    theme_id: Mapped[t.Optional[int]] = mapped_column(
        sa.ForeignKey("theme.id")
    )
    theme: Mapped[t.Optional["Theme"]] = relationship(back_populates="sets")

    # Year
    year_id: Mapped[t.Optional[int]] = mapped_column(sa.ForeignKey("year.id"))
    year: Mapped[t.Optional["Year"]] = relationship(back_populates="sets")

    # GenericSet
    parents: Mapped[t.List["GenericSet"]] = relationship(
        secondary="generic_set_rel",
        viewonly=True,
        foreign_keys="[GenericSetRelationship.child_id]",
    )
    children: Mapped[t.List["GenericSet"]] = relationship(
        secondary="generic_set_rel",
        viewonly=True,
        foreign_keys="[GenericSetRelationship.parent_id]",
    )

    # GenericSetRelationship
    parents_rel: Mapped[t.List["GenericSetRelationship"]] = relationship(
        viewonly=True, foreign_keys="[GenericSetRelationship.child_id]"
    )
    children_rel: Mapped[t.List["GenericSetRelationship"]] = relationship(
        viewonly=True, foreign_keys="[GenericSetRelationship.parent_id]"
    )

    # GenericSetPart
    parts: Mapped[t.List["GenericSetPart"]] = relationship(
        back_populates="set"
    )


# Parts
class PartCategory(db.Model):
    __tablename__ = "part_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))

    # Parts
    parts: Mapped[t.List["Part"]] = relationship(back_populates="category")


class Part(db.Model):
    __tablename__ = "part"

    id: Mapped[str] = mapped_column(sa.String(20), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    material: Mapped[str] = mapped_column(sa.String(255))

    # PartCategory
    category_id: Mapped[int] = mapped_column(
        sa.ForeignKey("part_category.id"), nullable=False
    )
    category: Mapped["PartCategory"] = relationship(back_populates="parts")

    # GenericSetPart
    inset: Mapped[t.List["GenericSetPart"]] = relationship(
        back_populates="part"
    )

    # Element
    elements: Mapped[t.List["Element"]] = relationship(back_populates="part")


class GenericSetPart(db.Model):
    __tablename__ = "generic_set_part"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column()
    is_spare: Mapped[bool] = mapped_column()
    img_url: Mapped[str] = mapped_column(sa.Text)

    # GenericSet
    set_id: Mapped[str] = mapped_column(
        sa.String, sa.ForeignKey("generic_set.id"), nullable=False
    )
    set: Mapped["GenericSet"] = relationship(back_populates="parts")

    # Part
    part_id: Mapped[str] = mapped_column(
        sa.String, sa.ForeignKey("part.id"), nullable=False
    )
    part: Mapped["Part"] = relationship(back_populates="inset")

    # Color
    color_id: Mapped[int] = mapped_column(
        sa.ForeignKey("color.id"), nullable=False
    )
    color: Mapped["Color"] = relationship(back_populates="parts")

    def get_related_elements(self):
        for element in self.part.elements:
            if element.color_id == self.color_id:
                yield element


# Element
class Element(db.Model):
    __tablename__ = "element"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Part
    part_id: Mapped[str] = mapped_column(
        sa.ForeignKey("part.id"), nullable=False
    )
    part: Mapped[Part] = relationship(back_populates="elements")

    # Color
    color_id: Mapped[int] = mapped_column(
        sa.ForeignKey("color.id"), nullable=False
    )
    color: Mapped[Color] = relationship(back_populates="elements")


# class PartsRelationship(db.Model):
#     __tablename__ = "parts_relationship"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     rel_type: Mapped[str] = mapped_column(sa.String(10))
#     child_part_id: Mapped[str] = mapped_column(sa.ForeignKey("part.part_num"))
#     parent_part_id: Mapped[str] = mapped_column(sa.ForeignKey("part.part_num"))

#     child_part: Mapped[Part] = relationship(foreign_keys=[child_part_id])
#     parent_part: Mapped[Part] = relationship(foreign_keys=[parent_part_id])
