"""

create table users

Revision ID: b527b3161830
Creation date: 2023-03-24 14:55:08.122511

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'b527b3161830'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        f"""--sql
        CREATE TABLE users(
            uid UUID DEFAULT gen_random_uuid() PRIMARY KEY,

            username TEXT NOT NULL,
            password TEXT NOT NULL,

            created_at TIMESTAMP WITH TIME ZONE NOT NULL,
            updated_at TIMESTAMP WITH TIME ZONE
        );
        """
    )

def downgrade() -> None:
    op.execute(
        f"""--sql
        DROP TABLE users;
        """
    )

