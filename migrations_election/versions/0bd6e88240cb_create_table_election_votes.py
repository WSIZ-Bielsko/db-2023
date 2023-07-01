"""

create table election_votes

Revision ID: 0bd6e88240cb
Creation date: 2023-06-23 18:10:58.086115

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '0bd6e88240cb'
down_revision = '872c69bf6349'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE TABLE election_votes(
        election_id UUID NOT NULL REFERENCES election ON DELETE CASCADE,
        choice_id UUID NOT NULL REFERENCES choice ON DELETE CASCADE,
        UNIQUE (election_id, choice_id)
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE election_votes CASCADE')
