"""

create table election

Revision ID: f303fe7aa382
Creation date: 2023-06-23 18:10:05.737740

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'f303fe7aa382'
down_revision = '9b4b3d1e7859'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE TABLE election(
        election_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
        type_id UUID NOT NULL REFERENCES election_type ON DELETE CASCADE,
        region_id UUID NOT NULL REFERENCES region ON DELETE CASCADE,
        vote_start TIMESTAMP NOT NULL DEFAULT NOW(),
        vote_end TIMESTAMP NOT NULL DEFAULT NOW()
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE election CASCADE')
