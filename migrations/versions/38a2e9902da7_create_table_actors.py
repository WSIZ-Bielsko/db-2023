"""

create table actors

Revision ID: 38a2e9902da7
Creation date: 2023-04-24 13:15:45.469648

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '38a2e9902da7'
down_revision = 'edbc25e8f3b0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE actors(
        actor_id SERIAL PRIMARY KEY,
        name TEXT
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS actors CASCADE;
    """)
