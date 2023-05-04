from db_services import DbService
from functions import *
from asyncio import *


async def createMovieCrew():
    db = DbService()
    await db.initialize()

    f = '../data/tmdb_5000_credits.csv'
    m_crew = get_movie_crew(f)

    for mc, mcr in enumerate(m_crew):
        await db.upsert_movie_crew(mcr)
        if mc % 100 == 0:
            print(f'import movie crew in {mc / len(m_crew) * 100:.1f}% done')

    await sleep(1)


if __name__ == "__main__":
    run(createMovieCrew())
