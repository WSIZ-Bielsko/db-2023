import json
import pandas as pd
from model import *

pd.options.display.max_rows = 6
df = pd.read_csv('../data/tmdb_5000_credits.csv')
crews = [x for x in df['crew']]
employees, ids = {}, {}
for crew in crews:
    for cr in json.loads(crew):
        crew = CrewEntry(movie_index=0, **cr)
        if crew.name not in employees: employees[crew.name] = {crew.id}
        else:
            if crew.id in ids and crew.name != ids.get(crew.id): raise Exception()
            ids[crew.id] = crew.name
            employees.get(crew.name).add(crew.id)

for crew_name, crew_id in list(employees.items()):
    if len(crew_id) > 2: print(f'{crew_name} = {crew_id}')
