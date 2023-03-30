"""

create table securedresource

Revision ID: 02bacce4e5ac
Creation date: 2023-03-30 20:19:27.743905

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '02bacce4e5ac'
down_revision = '7d22d35024a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE securedresource (
	resourceid SERIAL PRIMARY KEY,
	name TEXT NOT NULL UNIQUE,
	isopen BOOL DEFAULT TRUE NOT NULL
);
    """)


def downgrade() -> None:
    op.execute("""
     DROP TABLE securedresource;
    """)