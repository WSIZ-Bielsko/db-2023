"""

create table genres

Revision ID: e3042774f401
Creation date: 2023-04-29 12:53:02.608066

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'e3042774f401'
down_revision = '555cb0f59599'
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
