"""

create table security_group

Revision ID: bcc4ef251bad
Creation date: 2023-03-25 11:15:20.034891

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'bcc4ef251bad'
down_revision = '52f40fff095f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE security_group(
    group_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
    """)

def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS security_group CASCADE;
    """)