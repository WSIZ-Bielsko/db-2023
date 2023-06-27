"""

create table videos

Revision ID: b1f8a6bd4775
Creation date: 2023-06-27 12:12:53.093910

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'b1f8a6bd4775'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
CREATE TABLE videos (
  video_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL
);
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS videos CASCADE;
    """)
