"""

insert values

Revision ID: 44fd357c94f2
Creation date: 2023-03-30 20:41:11.544692

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '44fd357c94f2'
down_revision = '5623a04771d4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    INSERT INTO accesskey(name) VALUES ('abcd');
    INSERT INTO accesskey(name) VALUES ('dcba');
    INSERT INTO securedresource(name) VALUES ('qwerty');
    INSERT INTO securitygroup(groupname) VALUES ('hjkl'); 
    """)


def downgrade() -> None:
    op.execute("""  
    DELETE FROM accesskey WHERE keyid=1;
    DELETE FROM accesskey WHERE keyid=2;
    DELETE FROM securedresource WHERE resourceid=1;
    DELETE FROM securitygroup WHERE groupid=1;
    """)
