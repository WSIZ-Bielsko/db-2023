from asyncio import run, create_task, gather

from src.movies.analysis_tools import get_casts, get_actors, get_movies
from src.movies.db_service import DbService
from src.movies.model import Actor


async def create_movies():
    db = DbService()
    await db.initialize()

    movies = get_movies('data/tmdb_5000_movies.csv')
    print(f'all movies: {len(movies)}')
    tasks = []
    for i, m in enumerate(movies):
        tasks.append(create_task(db.upsert_movie(m)))
        if i % 100 == 0:
            print(f'import in {i / len(movies) * 100:.1f}% done')
    await gather(*tasks)
    print('all done')


if __name__ == '__main__':
    run(create_movies())
