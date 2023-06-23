"""

create table region

Revision ID: 9b4b3d1e7859
Creation date: 2023-06-23 18:10:23.842762

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '9b4b3d1e7859'
down_revision = '18b2ec774b45'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE TABLE region(
        region_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
        region_name TEXT NOT NULL UNIQUE CHECK(region_name ~ '^[ -~]{1,100}$')
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE region CASCADE')
