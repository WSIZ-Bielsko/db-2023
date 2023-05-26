"""

create table crew

Revision ID: bd886a6697b7
Creation date: 2023-05-25 10:38:15.595526

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'bd886a6697b7'
down_revision = 'a37516e59cdd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE crew(
            credit_id TEXT PRIMARY KEY, 
            movie_id int REFERENCES movies ON DELETE CASCADE,
            department text,
            gender int,
            id int,
            job text,
            name text
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE crew")

