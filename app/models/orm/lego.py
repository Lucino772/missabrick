from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.orm.base import Base
from app.models.orm.types import intpk, strpk


# Theme, Year & Color
class Theme(Base):
    __tablename__ = "theme"

    id: Mapped[intpk]  # noqa: A003
    name: Mapped[str]

    # Theme
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("theme.id"))
    parent: Mapped["Theme | None"] = relationship()

    # GenericSet
    sets: Mapped[list["GenericSet"]] = relationship(back_populates="theme")


class Year(Base):
    __tablename__ = "year"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    name: Mapped[int]

    # GenericSet
    sets: Mapped[list["GenericSet"]] = relationship(back_populates="year")


class Color(Base):
    __tablename__ = "color"

    id: Mapped[intpk]  # noqa: A003
    name: Mapped[str]
    rgb: Mapped[str] = mapped_column(String(20))
    is_trans: Mapped[bool]

    # GenericSetPart
    parts: Mapped[list["GenericSetPart"]] = relationship(back_populates="color")

    # Element
    elements: Mapped[list["Element"]] = relationship(back_populates="color")


# Sets (Set & Minifig)
class GenericSetRelationship(Base):
    __tablename__ = "generic_set_rel"

    quantity: Mapped[int]

    # GenericSet (Parent)
    parent_id: Mapped[str] = mapped_column(
        String, ForeignKey("generic_set.id"), primary_key=True
    )
    parent: Mapped["GenericSet"] = relationship(foreign_keys=[parent_id])

    # GenericSet (Child)
    child_id: Mapped[str] = mapped_column(
        String, ForeignKey("generic_set.id"), primary_key=True
    )
    child: Mapped["GenericSet"] = relationship(foreign_keys=[child_id])


class GenericSet(Base):
    __tablename__ = "generic_set"

    id: Mapped[strpk]  # noqa: A003
    name: Mapped[str]
    num_parts: Mapped[int]
    img_url: Mapped[str] = mapped_column(Text)
    is_minifig: Mapped[bool]

    # Theme
    theme_id: Mapped[int | None] = mapped_column(ForeignKey("theme.id"))
    theme: Mapped["Theme | None"] = relationship(back_populates="sets")

    # Year
    year_id: Mapped[int | None] = mapped_column(ForeignKey("year.id"))
    year: Mapped["Year | None"] = relationship(back_populates="sets")

    # GenericSet
    parents: Mapped[list["GenericSet"]] = relationship(
        secondary="generic_set_rel",
        viewonly=True,
        foreign_keys="[GenericSetRelationship.child_id]",
    )
    children: Mapped[list["GenericSet"]] = relationship(
        secondary="generic_set_rel",
        viewonly=True,
        foreign_keys="[GenericSetRelationship.parent_id]",
    )

    # GenericSetRelationship
    parents_rel: Mapped[list["GenericSetRelationship"]] = relationship(
        viewonly=True, foreign_keys="[GenericSetRelationship.child_id]"
    )
    children_rel: Mapped[list["GenericSetRelationship"]] = relationship(
        viewonly=True, foreign_keys="[GenericSetRelationship.parent_id]"
    )

    # GenericSetPart
    parts: Mapped[list["GenericSetPart"]] = relationship(back_populates="set")


# Parts
class PartCategory(Base):
    __tablename__ = "part_category"

    id: Mapped[intpk]  # noqa: A003
    name: Mapped[str]

    # Parts
    parts: Mapped[list["Part"]] = relationship(back_populates="category")


class Part(Base):
    __tablename__ = "part"

    id: Mapped[strpk]  # noqa: A003
    name: Mapped[str]
    material: Mapped[str]

    # PartCategory
    category_id: Mapped[int] = mapped_column(
        ForeignKey("part_category.id"), nullable=False
    )
    category: Mapped["PartCategory"] = relationship(back_populates="parts")

    # GenericSetPart
    inset: Mapped[list["GenericSetPart"]] = relationship(back_populates="part")

    # Element
    elements: Mapped[list["Element"]] = relationship(back_populates="part")


class GenericSetPart(Base):
    __tablename__ = "generic_set_part"

    id: Mapped[intpk]  # noqa: A003
    quantity: Mapped[int]
    is_spare: Mapped[bool]
    img_url: Mapped[str] = mapped_column(Text)

    # GenericSet
    set_id: Mapped[str] = mapped_column(
        String, ForeignKey("generic_set.id"), nullable=False
    )
    set: Mapped["GenericSet"] = relationship(back_populates="parts")  # noqa A003

    # Part
    part_id: Mapped[str] = mapped_column(String, ForeignKey("part.id"), nullable=False)
    part: Mapped["Part"] = relationship(back_populates="inset")

    # Color
    color_id: Mapped[int] = mapped_column(ForeignKey("color.id"), nullable=False)
    color: Mapped["Color"] = relationship(back_populates="parts")

    def get_related_elements(self):
        for element in self.part.elements:
            if element.color_id == self.color_id:
                yield element


# Element
class Element(Base):
    __tablename__ = "element"

    id: Mapped[intpk]  # noqa: A003

    # Part
    part_id: Mapped[str] = mapped_column(ForeignKey("part.id"), nullable=False)
    part: Mapped[Part] = relationship(back_populates="elements")

    # Color
    color_id: Mapped[int] = mapped_column(ForeignKey("color.id"), nullable=False)
    color: Mapped[Color] = relationship(back_populates="elements")


# class PartsRelationship(Base):
#     __tablename__ = "parts_relationship"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     rel_type: Mapped[str] = mapped_column(sa.String(10))
#     child_part_id: Mapped[str] = mapped_column(sa.ForeignKey("part.part_num"))
#     parent_part_id: Mapped[str] = mapped_column(sa.ForeignKey("part.part_num"))

#     child_part: Mapped[Part] = relationship(foreign_keys=[child_part_id])
#     parent_part: Mapped[Part] = relationship(foreign_keys=[parent_part_id])
