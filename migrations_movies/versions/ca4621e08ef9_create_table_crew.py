"""

create table crew

Revision ID: ca4621e08ef9
Creation date: 2023-05-02 22:03:29.167121

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'ca4621e08ef9'
down_revision = '03a94830a8ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        --sql
        create table crew
    (
        crew_id int,
        gender integer,
        name text,
        CONSTRAINT pk_crew PRIMARY KEY (crew_id, gender, name)
    );
        """)

def downgrade() -> None:
    op.execute(
        f"""--sql
        drop table if exists crew cascade
        """)