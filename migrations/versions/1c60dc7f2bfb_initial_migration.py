"""Initial migration

Revision ID: 1c60dc7f2bfb
Revises:
Create Date: 2023-04-22 16:05:46.960535

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision = "1c60dc7f2bfb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "color",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("rgb", sa.String(length=20), nullable=False),
        sa.Column("is_trans", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "minifig",
        sa.Column("fig_num", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("num_parts", sa.Integer(), nullable=False),
        sa.Column("img_url", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("fig_num"),
    )
    op.create_table(
        "parts_category",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "theme",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["theme.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=20), nullable=False),
        sa.Column(
            "email",
            sqlalchemy_utils.types.email.EmailType(length=255),
            nullable=False,
        ),
        sa.Column(
            "password",
            sqlalchemy_utils.types.password.PasswordType(max_length=1024),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_table(
        "part",
        sa.Column("part_num", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("part_material", sa.String(length=255), nullable=False),
        sa.Column("part_category_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["part_category_id"],
            ["parts_category.id"],
        ),
        sa.PrimaryKeyConstraint("part_num"),
    )
    op.create_table(
        "set",
        sa.Column("set_num", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("num_parts", sa.Integer(), nullable=False),
        sa.Column("img_url", sa.Text(), nullable=False),
        sa.Column("theme_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["theme_id"],
            ["theme.id"],
        ),
        sa.PrimaryKeyConstraint("set_num"),
    )
    op.create_table(
        "element",
        sa.Column("element_id", sa.Integer(), nullable=False),
        sa.Column("color_id", sa.Integer(), nullable=False),
        sa.Column("part_id", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(
            ["color_id"],
            ["color.id"],
        ),
        sa.ForeignKeyConstraint(
            ["part_id"],
            ["part.part_num"],
        ),
        sa.PrimaryKeyConstraint("element_id"),
    )
    op.create_table(
        "inventory",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("is_minifig", sa.Boolean(), nullable=False),
        sa.Column("set_id", sa.String(length=20), nullable=True),
        sa.Column("minifig_id", sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(
            ["minifig_id"],
            ["minifig.fig_num"],
        ),
        sa.ForeignKeyConstraint(
            ["set_id"],
            ["set.set_num"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "parts_relationship",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rel_type", sa.String(length=10), nullable=False),
        sa.Column("child_part_id", sa.String(length=20), nullable=False),
        sa.Column("parent_part_id", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(
            ["child_part_id"],
            ["part.part_num"],
        ),
        sa.ForeignKeyConstraint(
            ["parent_part_id"],
            ["part.part_num"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "inventory_minifigs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("inventory_id", sa.Integer(), nullable=False),
        sa.Column("minifig_id", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(
            ["inventory_id"],
            ["inventory.id"],
        ),
        sa.ForeignKeyConstraint(
            ["minifig_id"],
            ["minifig.fig_num"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "inventory_parts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("is_spare", sa.Boolean(), nullable=False),
        sa.Column("img_url", sa.Text(), nullable=False),
        sa.Column("inventory_id", sa.Integer(), nullable=False),
        sa.Column("part_id", sa.String(), nullable=False),
        sa.Column("color_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["color_id"],
            ["color.id"],
        ),
        sa.ForeignKeyConstraint(
            ["inventory_id"],
            ["inventory.id"],
        ),
        sa.ForeignKeyConstraint(
            ["part_id"],
            ["part.part_num"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "inventory_sets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("inventory_id", sa.Integer(), nullable=False),
        sa.Column("set_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["inventory_id"],
            ["inventory.id"],
        ),
        sa.ForeignKeyConstraint(
            ["set_id"],
            ["set.set_num"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("inventory_sets")
    op.drop_table("inventory_parts")
    op.drop_table("inventory_minifigs")
    op.drop_table("parts_relationship")
    op.drop_table("inventory")
    op.drop_table("element")
    op.drop_table("set")
    op.drop_table("part")
    op.drop_table("user")
    op.drop_table("theme")
    op.drop_table("parts_category")
    op.drop_table("minifig")
    op.drop_table("color")
    # ### end Alembic commands ###
