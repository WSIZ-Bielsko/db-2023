"""

add_columns_to_table_movies

Revision ID: f4f59c4f9147
Creation date: 2023-05-13 12:28:31.225543

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'f4f59c4f9147'
down_revision = 'f01147f524ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    alter table s9999movies.movies
    add budget bigint default 0,
    add popularity float default 0,
    add release_date date default '1000-01-01',
    add revenue bigint default 0;
    """)


def downgrade() -> None:
    op.execute("""
    alter table s9999movies.movies
    drop column budget,
    drop column popularity,
    drop column release_date,
    drop column revenue;
    """)
