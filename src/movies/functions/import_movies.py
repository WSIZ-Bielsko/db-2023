from db_services import DbService
from functions import *
from asyncio import *


async def createMovies():
    db = DbService()
    await db.initialize()

    movies = get_movies('../data/tmdb_5000_movies.csv')
    tasks = []
    for i, m in enumerate(movies):
        tasks.append(create_task(db.upsert_movie(m)))
        if i % 100 == 0:
            print(f'import in {i / len(movies) * 100:.1f}% done')
    await gather(*tasks)


if __name__ == "__main__":
    run(createMovies())
