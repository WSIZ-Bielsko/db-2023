"""create table files

Revision ID: 1b8334c826c9
Revises: 
Create Date: 2023-05-27 13:31:08.992942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b8334c826c9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
       create table if not exists files (
    file_id serial primary key,
    name text not null,
    bytes int check ( bytes >= 0 ),
    depth int check ( depth >= 0 ),
    accessed timestamp DEFAULT CURRENT_TIMESTAMP not null,
    modified timestamp DEFAULT CURRENT_TIMESTAMP not null,
    basename text not null,
    extension text,
    type text check (type IN ('d', 'f')),
    mode text not null ,
    parent_path text not null,
    full_path text not null
);
       """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS files CASCADE;
    """)