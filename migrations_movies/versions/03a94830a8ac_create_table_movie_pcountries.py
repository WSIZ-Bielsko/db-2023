"""

create table movie_pcountries

Revision ID: 03a94830a8ac
Creation date: 2023-04-29 10:15:28.383063

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '03a94830a8ac'
down_revision = '1dd498a89864'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE movie_pcountries(
    movie_id int references movies(movie_id) on delete cascade,
    iso_3166_1 varchar(2) references pcountries(iso_3166_1)on delete cascade
);
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS movie_pcountries CASCADE;
    """)


