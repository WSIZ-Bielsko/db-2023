import os
from asyncio import run, create_task, gather

from src.movies.analysis_tools import *
from src.movies.db_class import DbService
from src.movies.model import Actor


async def create_movie_crew():
    db = DbService()
    await db.initialize()

    mcrews = get_moviecrew()
    print(f'all moviecrews: {len(mcrews)}')
    tasks = []
    for i, m in enumerate(mcrews):
        tasks.append(create_task(db.upsert_movie_crews(m)))
        if i % 100 == 0:
            print(f'import in {i / len(mcrews) * 100:.1f}% done')
    await gather(*tasks)
    print('all done')


if __name__ == '__main__':
    run(create_movie_crew())