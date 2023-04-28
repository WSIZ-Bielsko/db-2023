"""create movie_prod_companies table

Revision ID: f460ea7b6e8f
Revises: 70d4a65eb2a5
Create Date: 2023-04-28 08:34:54.325602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f460ea7b6e8f'
down_revision = '70d4a65eb2a5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f"""
    --sql 
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
    op.execute(f"""
    DROP TABLE IF EXISTS movie_prod_companies CASCADE;
""")
