import json
import pandas as pd
from model import CastEntry


pd.options.display.max_rows = 10
df = pd.read_csv('../../../migrations/data/tmdb_5000_credits.csv')

casts = [x for x in df['cast']]  # lista wartości w kolumnie 'casts'
actors, ids = {}, {}
for cast in casts:
    for cs in json.loads(cast):
        cast = CastEntry(movie_index=0, **cs)
        if cast.name not in actors: actors[cast.name] = {cast.id}
        else:
            if cast.id in ids and cast.name != ids.get(cast.id): raise Exception()
            ids[cast.id] = cast.name
            actors.get(cast.name).add(cast.id)

for actor_name, actor_id in list(actors.items()):
    if len(actor_id) > 2: print(f'{actor_name} = {actor_id}')



# 2 pytania:
# 1) czy pole "id" jest unikalne dla danego aktora, czyli pola "name" (czyli: czy można interpretować "id" jako "actor_id")
# 2) czy pole "credit_id" jest unikalne wśród wszystkich filmów i elementów listy cast każdego z filmów...
#  (czyli: czy możnaby go w zasadzie traktować jako primary key w tabeli "Cast" którą będziemy tworzyli)
