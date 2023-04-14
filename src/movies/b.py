import json

import pandas as pd

from movies.model import CastEntry

pd.options.display.max_rows = 6

df = pd.read_csv('data/tmdb_5000_credits.csv')

# print(df.head())
print(df['cast'])

casts = [x for x in df['cast']]
print(type(casts[0]))  # str
w = json.loads(casts[0])    # list[dict]
for cs in w:
    print(CastEntry(**cs))
