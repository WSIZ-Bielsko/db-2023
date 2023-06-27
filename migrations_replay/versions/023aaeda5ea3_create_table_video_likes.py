"""

create table video_likes

Revision ID: 023aaeda5ea3
Creation date: 2023-06-27 12:23:28.470282

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '023aaeda5ea3'
down_revision = '4399345a6b07'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
CREATE TABLE video_likes (
  video_id UUID NOT NULL,
  user_id UUID NOT NULL,
  is_liked BOOLEAN NOT NULL,
  FOREIGN KEY (video_id) REFERENCES videos(video_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS video_likes CASCADE;
    """)
