from asyncio import run, sleep

from db_class import DbService
from src.movies.analysis_tools import *


async def main():
    db = DbService()
    await db.initialize()  # tu łączymy się z bazą danych

    pcountries = get_pcountries()
    print(len(pcountries))

    for i, pcountry in enumerate(pcountries):
        await db.upsert_pcountry(pcountry)
        if i % 100 == 0:
            print(f'import in {i / len(pcountries) * 100:.1f}% done')

    await sleep(1)
    print('all done')


if __name__ == '__main__':
    run(main())
