"""

dodanie wartosci do accesskey, securedresources, securitygroup

Revision ID: 5091197656d8
Creation date: 2023-03-25 11:08:04.858416

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '5091197656d8'
down_revision = 'b417e60eeac9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
insert into accesskey(name) values ('test');
insert into accesskey(name) values ('test2');
insert into securedresources(name, isopen) values ('test1', true);
insert into securitygroup(groupname) values ('grupa1');
        """
    )

def downgrade() -> None:
    op.execute(
        """
delete from securitygroup where securitygroup.groupname = 'grupa1';
delete from securedresources where securedresources.name = 'test1';
delete from accesskey where accesskey.name = 'test' or accesskey.name = 'test2';
        """
    )