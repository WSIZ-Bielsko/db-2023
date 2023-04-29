import asyncio
from asyncio import run, sleep

from db_class import DbService
from src.movies.analysis_tools import *


async def main():
    db = DbService()
    await db.initialize()  # tu łączymy się z bazą danych

    genres = get_movie_genres('data/tmdb_5000_movies.csv')
    tasks = []

    for i, genre in enumerate(genres):
        tasks.append(asyncio.create_task(db.upsert_movie_genre(genre.genre_id, genre.movie_id)))
        if i % 100 == 0:
            print(f'import in {i / len(genres) * 100:.1f}% done')
            await asyncio.gather(*tasks)
            tasks = []

    await asyncio.gather(*tasks)
    await sleep(1)
    print('all done')


if __name__ == '__main__':
    run(main())
