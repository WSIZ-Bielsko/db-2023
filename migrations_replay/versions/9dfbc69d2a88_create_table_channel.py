"""create table channel


Revision ID: 9dfbc69d2a88
Revises: 
Create Date: 2023-06-16 16:33:31.067717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dfbc69d2a88'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE channel(
    channel_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
    username TEXT UNIQUE NOT NULL CHECK(username ~ '^[ -~]{1,50}$')
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE channel;')
