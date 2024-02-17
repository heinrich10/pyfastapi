"""init persons and country db

Revision ID: 602af0699ee9
Revises:
Create Date: 2023-07-31 12:05:29.431998

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '602af0699ee9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "countries",
        sa.Column("code", sa.String(2), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("phone", sa.Integer, nullable=False),
        sa.Column("symbol", sa.String(10)),
        sa.Column("capital", sa.String(80)),
        sa.Column("currency", sa.String(3)),
        sa.Column("continent_code", sa.String(2), sa.ForeignKey("continents.code")),
        sa.Column("alpha_3", sa.String(3)),
    )
    op.create_table(
        "continents",
        sa.Column("code", sa.String(2), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
    )
    op.create_table(
        "persons",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("last_name", sa.String(100), nullable=True),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("country_code", sa.String(2), sa.ForeignKey("countries.code")),
    )


def downgrade() -> None:
    op.drop_table("countries")
    op.drop_table("continents")
    op.drop_table("persons")
