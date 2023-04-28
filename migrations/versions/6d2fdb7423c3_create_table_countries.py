"""create table countries

Revision ID: 6d2fdb7423c3
Revises: f460ea7b6e8f
Create Date: 2023-04-28 16:12:00.480357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d2fdb7423c3'
down_revision = 'f460ea7b6e8f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f"""
    --sQL
    CREATE TABLE countries(
        country_id VARCHAR(3) PRIMARY KEY UNIQUE NOT NULL,
        name TEXT
        );
""")


def downgrade() -> None:
    op.execute(f"""
    DROP TABLE IF EXISTS countries CASCADE;
""")