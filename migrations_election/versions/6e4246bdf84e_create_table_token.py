"""

create table token

Revision ID: 6e4246bdf84e
Creation date: 2023-06-23 18:10:37.857263

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '6e4246bdf84e'
down_revision = 'c007d92e3e9f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE TABLE token(
        token_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
        election_id UUID NOT NULL REFERENCES election ON DELETE CASCADE
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE token CASCADE')
