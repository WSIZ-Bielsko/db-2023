from asyncio import run, create_task, gather, sleep

from src.movies.db_service import DbService
from src.movies.import_tools import get_movies


async def import_movies():
    db = DbService()
    await db.initialize()

    movies = get_movies('data/tmdb_5000_movies.csv')
    tasks = []
    for i, m in enumerate(movies):
        tasks.append(create_task(db.upsert_movie(m)))
        if i % 100 == 0:
            print(f'import in {i / len(movies) * 100:.1f}% done')
            await gather(*tasks)
            tasks = []

    await gather(*tasks)
    print('all done')
    await sleep(1)


if __name__ == '__main__':
    run(import_movies())
