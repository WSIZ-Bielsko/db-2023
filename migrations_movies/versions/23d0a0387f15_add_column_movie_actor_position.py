"""

add column movie_actor.position

Revision ID: 23d0a0387f15
Creation date: 2023-05-25 14:14:31.577093

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '23d0a0387f15'
down_revision = 'bd886a6697b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("alter table movie_actors add column position int default 0;")
    op.execute("alter table movie_actors drop column order_;")


def downgrade() -> None:
    op.execute("alter table movie_actors drop column position;")
    op.execute("alter table movie_actors add column order_ int;")
