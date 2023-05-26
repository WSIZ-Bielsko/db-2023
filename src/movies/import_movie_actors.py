import asyncio
from asyncio import run, sleep

from db_service import DbService
from src.movies.import_tools import *


async def main():
    db = DbService()
    await db.initialize()  # tu łączymy się z bazą danych

    actors = get_movie_actors('data/tmdb_5000_credits.csv')

    print(f'all actors: {len(actors)}')
    tasks = []

    for i, actor in enumerate(actors):
        tasks.append(asyncio.create_task(db.upsert_movie_actor(actor)))
        if i % 100 == 0:
            print(f'import in {i / len(actors) * 100:.1f}% done')
            await asyncio.gather(*tasks)
            tasks = []
    await asyncio.gather(*tasks)

    await sleep(1)


if __name__ == '__main__':
    run(main())
