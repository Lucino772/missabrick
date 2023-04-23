"""Email Verification

Revision ID: ec626da6df08
Revises: 1c60dc7f2bfb
Create Date: 2023-04-23 01:05:40.483704

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ec626da6df08"
down_revision = "1c60dc7f2bfb"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("email_verified", sa.Boolean(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("email_verified_on", sa.DateTime(), nullable=True)
        )

    op.execute("UPDATE user SET email_verified = false")
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.alter_column("email_verified", nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("email_verified_on")
        batch_op.drop_column("email_verified")

    # ### end Alembic commands ###
