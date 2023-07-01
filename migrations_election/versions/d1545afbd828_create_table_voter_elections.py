"""

create table voter_elections

Revision ID: d1545afbd828
Creation date: 2023-06-23 18:11:25.433491

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'd1545afbd828'
down_revision = '0bd6e88240cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE TABLE voter_elections(
        election_id UUID NOT NULL REFERENCES election ON DELETE CASCADE,
        voter_id UUID NOT NULL REFERENCES voter ON DELETE CASCADE,
        UNIQUE (election_id, voter_id)
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE voter_elections CASCADE')