"""

create table actors

Revision ID: 116c259c1a33
Creation date: 2023-04-19 19:04:42.382112

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '116c259c1a33'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.execute("""
    create table actors(
       actor_id serial primary key,
       name text not null
    )
    """)

def downgrade() -> None:
    op.execute("""
    drop table actors;
    """)

