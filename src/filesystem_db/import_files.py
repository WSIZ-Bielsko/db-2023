import asyncio
import datetime
import time

import aiosqlite  # pip install aiosqlite
from model import File
from db_service import *


async def doit():
    async with aiosqlite.connect('data/database.sqlite') as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM files') as cursor:
            list_of_data = []
            async for row in cursor:
                file_id = row['fileid']
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
                file = File(file_id, name, bytes, depth, accessed, modified, basename, extension, type, mode,
                            parent_path, full_path)
                list_of_data.append(file)

            db = DbService()
            await db.initialize()

            print('all items:', len(list_of_data))
            tasks = []
            for i, item in enumerate(list_of_data):
                tasks.append(asyncio.create_task(db.upsert_file(item)))
                if i % 100 == 0:
                    print(f'import in {i / len(list_of_data) * 100:.1f}% done')
                    await asyncio.gather(*tasks)
                    tasks = []

            await asyncio.gather(*tasks)
            await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(doit())
