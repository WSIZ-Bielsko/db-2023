"""create table actors

Revision ID: 6226dc28417c
Revises: 3f00200a8956
Create Date: 2023-04-15 21:00:23.221782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6226dc28417c'
down_revision = '3f00200a8956'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f"""
    --sql 
    CREATE TABLE actors(
        actor_id SERIAL PRIMARY KEY,
        name TEXT                
    );
""")


def downgrade() -> None:
    op.execute(f"""
    --sql
    DROP TABLE actors;
""")
