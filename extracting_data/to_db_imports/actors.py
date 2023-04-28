from asyncio import run, sleep
from ..functions import get_cast, get_actors_of_movie, get_movie_actors
from ..db_service import DbService
from ..model import Actor


#ONLY ACTORS -------------------
async def create_actors():
    db = DbService()
    await db.initialize() # == establishing connection

    casts_ = get_cast()
    actors = get_actors_of_movie(casts_)
    actors = [Actor(*a) for a in actors]

    for a, actor in enumerate(actors):
        await db.upsert_actor(actor)
        if a%100 == 0:
            print(f'import actors in {a/ len(actors)*100:.1f}% done')

    await sleep(1)

#MOVIE ACTORS -------------------
async def create_movie_actors():
    db = DbService()
    await db.initialize() # == establishing connection

    filename = './datas/tmdb_5000_credits.csv'
    movie_actors = get_movie_actors(filename)

    for ma, mactor in enumerate(movie_actors):
        await db.upsert_movie_actor(mactor)
        if ma% 100== 0:
            print(f'import movie_actors in {ma/ len(movie_actors)*100:.1f}% done')

    await sleep(1)



if __name__ == "__main__":
    # run(create_actors())
    run(create_movie_actors())

    # get_cast()

