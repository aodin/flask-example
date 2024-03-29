"""Added permissions

Revision ID: 9b8db7ee069f
Revises: 82c2ee425d55
Create Date: 2023-03-10 13:33:24.991364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9b8db7ee069f"
down_revision = "82c2ee425d55"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Create private schema
    op.execute("create schema private")
    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="private",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("permissions", schema="private")
    # Drop private schema
    op.execute("drop schema private")
    # ### end Alembic commands ###
