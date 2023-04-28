"""

dodanie users

Revision ID: 8f2cc22eb003
Creation date: 2023-03-25 11:01:07.590437

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '8f2cc22eb003'
down_revision = 'e120aeca0fb1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        insert into users(username, password, created_at) values ('test1', 'test', current_date), ('test2', 'test', current_date), ('test3', 'test', current_date);
        """
    )

def downgrade() -> None:
    op.execute(
        """
        delete from users where username='test1' or username = 'test2' or username = 'test3';
        """
    )
