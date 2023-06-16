"""create table video_flags

Revision ID: a59fb02eae9e
Revises: 1763b143d9ca
Create Date: 2023-06-16 16:34:04.922690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a59fb02eae9e'
down_revision = '1763b143d9ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE video_flags(
    video_id UUID NOT NULL UNIQUE REFERENCES video(video_id),
    channel_id UUID NOT NULL UNIQUE REFERENCES channel(channel_id)
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE video_flags CASCADE')
