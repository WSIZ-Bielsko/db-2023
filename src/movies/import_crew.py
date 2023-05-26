import asyncio
from asyncio import run, sleep, create_task

from db_service import DbService
from src.movies.import_tools import *


async def main():
    db = DbService()
    await db.initialize()

    crew = get_crews(filename='data/tmdb_5000_credits.csv')

    print(f'all crews: {len(crew)}')
    tasks = []

    for i, c in enumerate(crew):
        tasks.append(create_task(db.upsert_crew(c)))
        if i % 100 == 0:
            await asyncio.gather(*tasks)
            tasks = []
            print(f'import in {i / len(crew) * 100:.1f}% done')

    await asyncio.gather(*tasks)

    await sleep(1)


if __name__ == '__main__':
    run(main())
