"""

create table group_resource

Revision ID: 55f85691121c
Creation date: 2023-03-25 11:15:52.443374

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '55f85691121c'
down_revision = '8e6d4746e66f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE group_resource(
    group_id UUID REFERENCES security_group(group_id) ON DELETE CASCADE,
    resource_id UUID REFERENCES secured_resource(resource_id) ON DELETE CASCADE
);
    """)

def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS group_resource CASCADE;
    """)
