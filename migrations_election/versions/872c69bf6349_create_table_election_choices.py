"""

create table election_choices

Revision ID: 872c69bf6349
Creation date: 2023-06-23 18:10:53.625671

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '872c69bf6349'
down_revision = '6e4246bdf84e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE TABLE election_choices(
        election_id UUID NOT NULL REFERENCES election ON DELETE CASCADE,
        choice_id UUID NOT NULL REFERENCES choice ON DELETE CASCADE,
        UNIQUE (election_id, choice_id)
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE election_choices CASCADE')
