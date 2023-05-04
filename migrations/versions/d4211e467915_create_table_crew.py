"""

create table crew

Revision ID: d4211e467915
Creation date: 2023-04-27 16:48:40.945349

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'd4211e467915'
down_revision = '642fdaaf1179'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE crew(
        person_id SERIAL PRIMARY KEY,
        name TEXT
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS crew CASCADE;
    """)
