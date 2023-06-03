"""

create table files

Revision ID: d1bee2b521b0
Creation date: 2023-06-02 14:32:55.718091

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'd1bee2b521b0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
       create table if not exists files (
            file_id SERIAL PRIMARY KEY,
            name text NOT NULL,
            bytes int CHECK ( bytes >= 0 ),
            depth int CHECK ( depth >= 0 ),
            accessed timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
            modified timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
            basename TEXT NOT NULL,
            extension TEXT,
            type TEXT CHECK (type IN ('d', 'f')),
            mode TEXT NOT NULL CHECK(mode ~ '^[d-]([r-][w-][x-]){3}$'),
            parent_path TEXT NOT NULL,
            full_path TEXT UNIQUE NOT NULL CHECK(full_path LIKE parent_path || name || '%')
        );
       """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS files CASCADE;
    """)
