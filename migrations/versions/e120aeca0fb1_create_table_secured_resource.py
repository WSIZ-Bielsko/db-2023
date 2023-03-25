"""

create table secured_resource

Revision ID: e120aeca0fb1
Creation date: 2023-03-25 10:29:29.578667

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'e120aeca0fb1'
down_revision = '1fd4316e4e74'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE secured_resource(
    resource_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    is_open BOOL DEFAULT TRUE NOT NULL
);
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS secured_resource CASCADE;
    """)