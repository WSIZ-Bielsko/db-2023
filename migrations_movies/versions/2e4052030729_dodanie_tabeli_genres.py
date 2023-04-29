"""

dodanie tabeli genres

Revision ID: 2e4052030729
Creation date: 2023-04-22 13:09:25.817765

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '2e4052030729'
down_revision = 'aed1fafe8100'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE genres(
    genre_id serial NOT NULL unique PRIMARY KEY,
    name TEXT NOT NULL
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS genres CASCADE;
    """)