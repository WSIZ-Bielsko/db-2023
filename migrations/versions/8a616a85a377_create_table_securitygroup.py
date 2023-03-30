"""

create table securitygroup

Revision ID: 8a616a85a377
Creation date: 2023-03-30 20:22:28.527560

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '8a616a85a377'
down_revision = '02bacce4e5ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE securitygroup(
        groupid SERIAL PRIMARY KEY,
        groupname TEXT NOT NULL UNIQUE
        );
        """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE securitygroup;
    """)
