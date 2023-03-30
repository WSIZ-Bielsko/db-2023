"""

create table groupkey

Revision ID: 237f892e4fd0
Creation date: 2023-03-30 20:25:41.764082

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '237f892e4fd0'
down_revision = '8a616a85a377'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE groupkey (
        groupid INT REFERENCES securitygroup(groupid),
        keyid INT REFERENCES accesskey(keyid),
        CONSTRAINT groupkey_pk PRIMARY KEY (groupid, keyid)
        );
        """)


def downgrade() -> None:
    op.execute("""
     DROP TABLE group_key;
     """)
