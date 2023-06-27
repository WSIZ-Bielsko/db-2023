"""create table files

Revision ID: 344fd686b41c
Revises: 
Create Date: 2023-05-27 12:54:34.441545

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '344fd686b41c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE files (
    file_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    bytes INT CHECK (bytes >= 0),
    depth INT CHECK (depth >= 0),
    accessed TIMESTAMP,
    modified TIMESTAMP,
    basename TEXT,
    extension TEXT,
    type CHAR(1) CHECK (type IN ('d', 'f')),
    mode TEXT NOT NULL,
    parent_path TEXT,
    full_path TEXT NOT NULL UNIQUE CHECK (full_path like files.parent_path || '%')
);
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS files CASCADE;
    """)
