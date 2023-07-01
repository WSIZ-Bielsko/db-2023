"""

create table voter

Revision ID: c007d92e3e9f
Creation date: 2023-06-23 18:10:34.927247

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'c007d92e3e9f'
down_revision = 'f303fe7aa382'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE TABLE voter(
        voter_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
        voter_name TEXT NOT NULL UNIQUE CHECK(voter_name ~ '^[ -~]{1,100}$')
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE voter CASCADE')
