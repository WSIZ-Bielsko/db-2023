"""

create table movies

Revision ID: 480c8a896701
Creation date: 2023-04-21 14:59:59.882657

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '480c8a896701'
down_revision = '116c259c1a33'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    create table movies(
        movie_id serial primary key,
        title text
    )
    """)


def downgrade() -> None:
    op.execute("""
    drop table movies
    """)
