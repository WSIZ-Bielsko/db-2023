"""

create table group_key

Revision ID: 8e6d4746e66f
Creation date: 2023-03-25 11:15:44.439111

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '8e6d4746e66f'
down_revision = 'bcc4ef251bad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE group_key(
    group_id UUID REFERENCES security_group(group_id) ON DELETE CASCADE,
    key_id UUID REFERENCES access_key(key_id) ON DELETE CASCADE
);
    """)

def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS group_key CASCADE;
    """)
