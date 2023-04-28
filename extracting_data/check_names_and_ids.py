"""
czy pole "id" jest unikalne dla danego aktora, czyli pola "name"
(czyli: czy można interpretować "id" jako "actor_id")
czy pole "credit_id" jest unikalne wśród wszystkich filmów i elementów listy cast każdego z filmów...
(czyli: czy możnaby go w zasadzie traktować jako primary key w tabeli "Cast" którą będziemy tworzyli)
"""

from collections import defaultdict
from functions import get_crew_of_movie, get_cast_of_movie

"""
NOTE: object CrewEntry and CastEntry were different while using these functions
"""
# CREW ----------------------
def check_assignment_crew(crew: list[str]):

    name_id_pairs = []
    for i, movie in enumerate(crew):
        entries = get_crew_of_movie(i, movie)
        for e in entries:
            print(e)
        name_id_pairs.extend([(c.id, c.name) for c in entries])

    unique_pairs = set(name_id_pairs)
    n_pairs = len(unique_pairs)
    n_names = len(set([c for i, c in unique_pairs]))  # unique names
    n_ids = len(set([i for i, c in unique_pairs]))  # unique id's

    print(f'{n_pairs=}')
    print(f'{n_ids=}')
    print(f'{n_names=}')

def find_duplicates_crew(crews: list[str]):
    name_id_pairs =[]
    for i, movie in enumerate(crews):
        entries = get_crew_of_movie(i, movie)
        name_id_pairs.extend([(c.id, c.name) for c in entries]) #comprehension

    unique_pairs = set(name_id_pairs)
    id_to_name = defaultdict(lambda : set())
    for (id, name) in unique_pairs:
        id_to_name[id].add(name)

    for (k, v) in id_to_name.items():
        if len(v) > 1:
            print('name -> ids: ', k, v)

    # -----
    name_to_id = defaultdict(lambda : set())
    for (id, name) in unique_pairs:
        name_to_id[name].add(id)

    for (k,v) in name_to_id.items():
        if len(v) > 4:
            print('name -> ids: ', k, v)

# CAST ----------------------
def check_unique_cast_credit_id(casts: list[str]):
    credit_ids = []
    for i, movie in enumerate(casts):
        entries = get_cast_of_movie(i, movie)
        credit_ids.extend([c.credit_id for c in entries])

    unique = (len(credit_ids) == len(set(credit_ids)))
    print(f'{unique=}')

def check_assignment_cast(cast: list[str]):

    name_id_pairs = []

    for i, movie in enumerate(cast):
        entries = get_cast_of_movie(i, movie)
        for e in entries:
            print(e)
        name_id_pairs.extend([(c.id, c.name) for c in entries])

    unique_pairs = set(name_id_pairs)
    n_pairs = len(unique_pairs)
    n_names = len(set([c for i, c in unique_pairs]))  # unique names
    n_ids = len(set([i for i, c in unique_pairs]))  # unique id's

    print(f'{n_pairs=}')
    print(f'{n_ids=}')
    print(f'{n_names=}')

    def find_duplicates_cast(casts: list[str]):
        name_id_pairs = []
        for i, movie in enumerate(casts):
            entries = get_cast_of_movie(i, movie)
            name_id_pairs.extend([(c.id, c.name) for c in entries])

        unique_pairs = set(name_id_pairs)
        id_to_name = defaultdict(lambda: set())
        for (id, name) in unique_pairs:
            id_to_name[id].add(name)

        for (k, v) in id_to_name.items():
            if len(v) > 1:
                print('id->names ', k, v)

        # -----
        name_to_id = defaultdict(lambda: set())
        for (id, name) in unique_pairs:
            name_to_id[name].add(id)

        for (k, v) in name_to_id.items():
            if len(v) > 4:
                print('name->ids ', k, v)

