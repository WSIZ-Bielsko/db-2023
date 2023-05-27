import asyncio
from asyncio import create_task

import aiosqlite    # pip install aiosqlite

from model import *
from db_service import *

async def doit():
    async with aiosqlite.connect('data/database.sqlite') as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM files limit 10') as cursor:
            listOfFiles = []
            async for row in cursor:
                fileid = row['fileid']
                name = row['name']
                bytes = row['bytes']
                depth = row['depth']
                accessed = datetime.strptime(row['accessed'], "%Y-%m-%dT%H:%M:%S")
                modified = datetime.strptime(row['modified'], "%Y-%m-%dT%H:%M:%S")
                basename = row['basename']
                extension = row['extension']
                type = row['type']
                mode = row['mode']
                parent_path = row['parentpath']
                full_path = row['fullpath']
                file = File(fileid, name, bytes, depth, accessed, modified, basename, extension, type, mode, parent_path, full_path)
                listOfFiles.append(file)

            db = DbService()
            await db.initialize()  # tu łączymy się z bazą danych

            print('all genres: ', len(listOfFiles))
            tasks = []

            for i, genre in enumerate(listOfFiles):
                tasks.append(create_task(db.upsert_file(genre)))
                if i % 100 == 0:
                    print(f'import in {i / len(listOfFiles) * 100:.1f}% done')
                    await asyncio.gather(*tasks)
                    tasks = []

            await asyncio.gather(*tasks)
            await db.update_serial()

            await sleep(1)


async def addFile(name: str, where: str, type: str = "", mode: str = "", bytes: int = 0):
    db = DbService()
    await db.initialize()  # tu łączymy się z bazą danych

    await db.create_file(where, name, type, mode, bytes)

    await sleep(1)


if __name__ == '__main__':
    # asyncio.run(doit())

    asyncio.run(addFile("aaa.py", "/Users/peterdalloz/gutenberg/epub/"))
