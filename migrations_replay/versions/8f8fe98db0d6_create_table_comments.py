"""

create table comments

Revision ID: 8f8fe98db0d6
Creation date: 2023-06-27 12:25:08.252255

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '8f8fe98db0d6'
down_revision = '023aaeda5ea3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
CREATE TABLE comments (
  comment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id UUID NOT NULL,
  user_id UUID NOT NULL,
  content TEXT NOT NULL,
  parent_id UUID,
  FOREIGN KEY (video_id) REFERENCES videos(video_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (parent_id) REFERENCES comments(comment_id)
);
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS comments CASCADE;
    """)
