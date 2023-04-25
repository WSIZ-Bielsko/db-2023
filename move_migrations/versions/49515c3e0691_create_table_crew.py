"""

create table crew

Revision ID: 49515c3e0691
Creation date: 2023-04-25 20:15:55.124500

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '49515c3e0691'
down_revision = '98a89320eb98'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        --sql
        create table crew
    (
        crew_id serial NOT NULL unique PRIMARY KEY,
        credit_id text,
        department text,
        gender integer,
        job text,
        name text
    );
        """)

def downgrade() -> None:
    op.execute(
        f"""--sql
        drop table if exists crew cascade
        """)