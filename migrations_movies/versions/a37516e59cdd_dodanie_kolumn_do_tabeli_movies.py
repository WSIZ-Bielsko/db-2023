"""

dodanie kolumn do tabeli movies

Revision ID: a37516e59cdd
Creation date: 2023-05-13 12:26:18.367831

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'a37516e59cdd'
down_revision = '03a94830a8ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
     ALTER TABLE movies
        ADD COLUMN budget int,
        ADD COLUMN popularity float,
        ADD COLUMN release_date date,
        ADD COLUMN revenue int;
     """)


def downgrade() -> None:
    op.execute("""
    ALTER TABLE movies
        DROP COLUMN budget,
        DROP COLUMN popularity,
        DROP COLUMN release_date,
        DROP COLUMN revenue;
    """)