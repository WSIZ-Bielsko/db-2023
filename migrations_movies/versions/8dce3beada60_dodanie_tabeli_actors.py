"""

dodanie tabeli actors

Revision ID: 8dce3beada60
Creation date: 2023-04-15 13:30:57.719199

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '8dce3beada60'
down_revision = 'e326cbf3e3e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE actors(
    actor_id int NOT NULL unique PRIMARY KEY,
    name TEXT NOT NULL
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS actors CASCADE;
    """)