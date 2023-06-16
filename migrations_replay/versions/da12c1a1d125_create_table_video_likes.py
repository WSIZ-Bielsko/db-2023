"""create table video_likes

Revision ID: da12c1a1d125
Revises: d84325290942
Create Date: 2023-06-16 16:33:50.840025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da12c1a1d125'
down_revision = 'd84325290942'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE video_likes(
    video_id UUID NOT NULL REFERENCES video(video_id),
    channel_id UUID NOT NULL REFERENCES channel(channel_id),
    is_like BOOLEAN NOT NULL
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE video_likes')
