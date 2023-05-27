from asyncio import run, sleep
from db_service import DbService
from sqlite import SQLite


async def main():
    db = DbService()
    sqlite = SQLite()
    await sqlite.initialize()
    await db.initialize()  # tu łączymy się z bazą danych

    files = await sqlite.get_files(222000)
    print(f'all files: {len(files)}')

    for i, a in enumerate(files):
        await db.upsert_file(a)
        if i % 100 == 0:
            print(f'import in {i / len(files) * 100:.1f}% done')

    await sleep(1)


if __name__ == '__main__':
    run(main())
