"""

create table groupresource

Revision ID: 5623a04771d4
Creation date: 2023-03-30 20:37:26.172119

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '5623a04771d4'
down_revision = '237f892e4fd0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE groupresource (
            groupid INT REFERENCES securitygroup(groupid),
            resourceid INT REFERENCES securedresource(resourceid),
            CONSTRAINT groupresource_pk PRIMARY KEY (groupid, resourceid)
            );
    """)


def downgrade() -> None:
    op.execute("""
   DROP TABLE group_resource;
   """)
