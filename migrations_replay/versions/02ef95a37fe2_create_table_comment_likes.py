"""create table comment_likes

Revision ID: 02ef95a37fe2
Revises: b4c4604cea97
Create Date: 2023-06-16 16:35:06.396545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02ef95a37fe2'
down_revision = 'b4c4604cea97'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE comment_likes(
    comment_id UUID NOT NULL UNIQUE REFERENCES comment(comment_id),
    channel_id UUID NOT NULL UNIQUE REFERENCES channel(channel_id),
    is_like BOOLEAN NOT NULL
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE comment_likes CASCADE')
