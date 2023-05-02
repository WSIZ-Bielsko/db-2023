import os
from asyncio import run, create_task, gather

from src.movies.analysis_tools import *
from src.movies.db_class import DbService
from src.movies.model import Crew


async def create_crew():
    db = DbService()
    await db.initialize()

    crews = get_crew()
    print(f'all crew: {len(crews)}')
    tasks = []
    for i, m in enumerate(crews):
        tasks.append(create_task(db.upsert_crew(m)))
        if i % 100 == 0:
            print(f'import in {i / len(crews) * 100:.1f}% done')
    await gather(*tasks)
    print('all done')


if __name__ == '__main__':
    run(create_crew())