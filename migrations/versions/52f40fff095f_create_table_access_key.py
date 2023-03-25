"""

create table access_key

Revision ID: 52f40fff095f
Creation date: 2023-03-25 11:12:45.530745

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '52f40fff095f'
down_revision = 'e120aeca0fb1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE access_key(
    key_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
    """)

def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS access_key CASCADE;
    """)
