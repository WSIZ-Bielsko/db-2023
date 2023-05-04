from db_services import DbService
from functions import *
from asyncio import *


async def createMovieActors():
    db = DbService()
    await db.initialize()

    f = '../data/tmdb_5000_credits.csv'
    m_actors = get_movie_actors(f)

    for ma, mact in enumerate(m_actors):
        await db.upsert_movie_actor(mact)
        if ma % 100 == 0:
            print(f'import movie_actors in {ma / len(m_actors) * 100:.1f}% done')

    await sleep(1)


if __name__ == "__main__":
    run(createMovieActors())
