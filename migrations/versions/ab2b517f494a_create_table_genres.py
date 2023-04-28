"""create table genres

Revision ID: ab2b517f494a
Revises: 74ffe47131fe
Create Date: 2023-04-28 16:18:23.014473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab2b517f494a'
down_revision = '74ffe47131fe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE genres(
    genre_id serial NOT NULL unique PRIMARY KEY,
    name TEXT NOT NULL
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS genres CASCADE;
    """)
