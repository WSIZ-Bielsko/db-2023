"""

create table prod companies

Revision ID: d2f971ee984c
Creation date: 2023-04-29 12:50:24.261184

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'd2f971ee984c'
down_revision = 'ab6bc702b84f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE prod_companies(
        company_id SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name TEXT NOT NULL
        );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS prod_companies CASCADE;
    """)
