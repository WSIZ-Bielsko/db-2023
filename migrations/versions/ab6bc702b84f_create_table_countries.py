"""

create table countries

Revision ID: ab6bc702b84f
Creation date: 2023-04-29 12:48:57.173429

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'ab6bc702b84f'
down_revision = 'dd67f214d8e8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE countries(
        country_id VARCHAR(3) PRIMARY KEY UNIQUE NOT NULL,
        name TEXT
        );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS countries CASCADE;
    """)
