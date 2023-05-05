from db_services import DbService
from functions import *
from asyncio import *


async def createCounties():
    db = DbService()
    await db.initialize()

    f = '../data/tmdb_5000_movies.csv'
    countries = get_countries(f)

    for c, country in enumerate(countries):
        await db.upsert_country(country)
        if c % 100 == 0:
            print(f'import countries in {c / len(countries) * 100:.1f}% done')

    await sleep(1)


if __name__ == "__main__":
    run(createCounties())
