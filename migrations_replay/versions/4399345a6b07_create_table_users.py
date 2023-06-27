"""

create table users

Revision ID: 4399345a6b07
Creation date: 2023-06-27 12:18:03.125893

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '4399345a6b07'
down_revision = 'b1f8a6bd4775'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
CREATE TABLE users (
  user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username TEXT NOT NULL
);
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS users CASCADE;
    """)
