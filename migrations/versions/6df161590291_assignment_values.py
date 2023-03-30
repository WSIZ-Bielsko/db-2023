"""

assignment values

Revision ID: 6df161590291
Creation date: 2023-03-30 20:53:06.655688

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '6df161590291'
down_revision = '44fd357c94f2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    INSERT INTO groupresource (groupid, resourceid) VALUES (6, 6);
    INSERT INTO groupkey (groupid, keyid) VALUES (6, 12);
    INSERT INTO groupkey (groupid, keyid) VALUES (6, 13);
    """)


def downgrade() -> None:
    op.execute("""
    DELETE FROM groupkey WHERE groupid=6;
    DELETE FROM groupresource WHERE groupid=6;
    """)
