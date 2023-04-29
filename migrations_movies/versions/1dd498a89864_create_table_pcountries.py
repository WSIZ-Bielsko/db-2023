"""

create table pcountries

Revision ID: 1dd498a89864
Creation date: 2023-04-29 09:14:36.876910

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '1dd498a89864'
down_revision = 'b355e311da60'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
       CREATE TABLE pcountries(
        iso_3166_1 TEXT PRIMARY KEY,
        name TEXT
       );
       """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS pcountries CASCADE;
    """)



