from db_services import DbService
from functions import *
from asyncio import *


async def createMovieCounties():
    db = DbService()
    await db.initialize()

    f = '../data/tmdb_5000_movies.csv'
    m_countries = get_movie_country(f)

    for mc, mcountry in enumerate(m_countries):
        await  db.upsert_movie_country(MovieCountry(movie_id=mcountry.movie_id,
                                                    country_id=mcountry.country_id))
        if mc % 100 == 0:
            print(f'import movie_countries in {mc / len(m_countries) * 100:.1f}% done')

    await sleep(1)


if __name__ == "__main__":
    run(createMovieCounties())
