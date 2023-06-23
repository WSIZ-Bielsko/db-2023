"""

create table election_type

Revision ID: 18b2ec774b45
Creation date: 2023-06-23 18:10:03.357704

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '18b2ec774b45'
down_revision = 'be1d45e00431'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""CREATE TABLE election_type(
        type_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
        type_name TEXT NOT NULL UNIQUE CHECK(type_name ~ '^[ -~]{1,100}$'),
        no_of_choices INT NOT NULL CHECK(no_of_choices > 0)
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE election_type CASCADE')
