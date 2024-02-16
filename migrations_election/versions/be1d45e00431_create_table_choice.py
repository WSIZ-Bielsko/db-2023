"""

create table choice

Revision ID: be1d45e00431
Creation date: 2023-06-23 18:09:56.562162

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'be1d45e00431'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE TABLE choice(
        choice_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
        choice_name TEXT NOT NULL UNIQUE CHECK(choice_name ~ '^[ -~]{1,100}$'),
        image TEXT NOT NULL CHECK(image ~ '^[ -~]{1,100}$')
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE choice CASCADE')
