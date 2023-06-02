from asyncio import run, sleep, create_task, gather

from db_service import DbService
from src.movies.import_tools import *


async def main():
    db = DbService()
    await db.initialize()

    actors = get_actors(filename='data/tmdb_5000_credits.csv')

    print(f'all actors: {len(actors)}')
    tasks = []

    for i, a in enumerate(actors):
        tasks.append(create_task(db.upsert_actor(a)))
        if i % 100 == 0:
            print(f'import in {i / len(actors) * 100:.1f}% done')
            await gather(*tasks)
            tasks = []

    await sleep(1)


if __name__ == '__main__':
    run(main())
