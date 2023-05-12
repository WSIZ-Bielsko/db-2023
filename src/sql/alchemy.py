import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv


load_dotenv()
engine = create_engine(os.getenv('DATABASE_URL'))
schema_name = os.getenv('SCHEMA')

query = f"SELECT * FROM {schema_name}.movie_crew"
pd.set_option('display.max_columns', None)
# pd.reset_option('max_columns')

df = pd.read_sql_query(query, engine).head()
print(df)
