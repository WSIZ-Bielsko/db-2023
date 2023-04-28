"""create table languages

Revision ID: b687107fac13
Revises: 0b7c0671dab0
Create Date: 2023-04-24 08:13:52.482652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b687107fac13'
down_revision = '0b7c0671dab0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f"""
    --sql 
    CREATE TABLE languages (
        lang_id VARCHAR(2) UNIQUE PRIMARY KEY,
        lang TEXT NOT NULL
    )

""")


def downgrade() -> None:
    op.execute(f"""
    DROP TABLE IF EXISTS languages CASCADE;
""")
