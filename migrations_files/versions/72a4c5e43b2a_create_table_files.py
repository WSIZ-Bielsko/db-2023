"""

create table files

Revision ID: 72a4c5e43b2a
Creation date: 2023-05-27 12:34:48.248011

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '72a4c5e43b2a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
       create table files
        (
            fileid     serial not null PRIMARY KEY,
            name       TEXT       not null,
            bytes      INT        not null,
            depth      INT,
            accessed   timestamp,
            modified   timestamp,
            basename   TEXT,
            extension  TEXT,
            type       TEXT,
            mode       TEXT,
            parentpath TEXT,
            fullpath   TEXT,
            CONSTRAINT check_fullpath_parentpath CHECK (fullpath LIKE parentpath || '%')
        );
       """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS files CASCADE;
    """)