"""create prod_companies table

Revision ID: 70d4a65eb2a5
Revises: 55a4fac8159e
Create Date: 2023-04-28 08:33:02.735673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70d4a65eb2a5'
down_revision = '55a4fac8159e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f"""
    --sql
    CREATE TABLE prod_companies(
        company_id SERIAL PRIMARY KEY UNIQUE NOT NULL,
        name TEXT NOT NULL
        );
""")


def downgrade() -> None:
    op.execute(f"""
    DROP TABLE IF EXISTS prod_companies CASCADE;
""")
