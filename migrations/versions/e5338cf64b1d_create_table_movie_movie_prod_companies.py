"""

create table movie movie prod companies

Revision ID: e5338cf64b1d
Creation date: 2023-04-29 12:56:30.569166

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'e5338cf64b1d'
down_revision = 'a4775aa32a71'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE movie_prod_companies(
        movie_id INT,
        company_id INT,
        
        CONSTRAINT fk_movie_id FOREIGN KEY (movie_id)
            REFERENCES movies(movie_id),
        CONSTRAINT fk_company_id FOREIGN KEY (company_id)
            REFERENCES prod_companies(company_id) 
            );  
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS movie_prod_companies CASCADE;
    """)
