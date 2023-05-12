"""

dodanie tabeli crew

Revision ID: 7709e579a6fa
Creation date: 2023-05-12 17:31:55.342279

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '7709e579a6fa'
down_revision = '03a94830a8ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    create table crew(
       crew_id int primary key,
       name text not null
    )
    """)

def downgrade() -> None:
    op.execute("""
    drop table crew;
    """)