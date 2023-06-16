import asyncio
from asyncio import sleep, create_task

import aiosqlite

from filesystem_db.db_service import DbService
from filesystem_db.model import *


async def do_import(db_file: str):
    async with aiosqlite.connect(db_file) as db:

        # logic: load all files, then save to DB
        # if memory is tight -- should
        db.row_factory = aiosqlite.Row
        all_files = []
        async with db.execute('SELECT * FROM files') as cursor:
            async for row in cursor:
                fileid = row['fileid']
                name = row['name']
                bytes_ = row['bytes']
                depth = row['depth']
                accessed = datetime.strptime(row['accessed'], "%Y-%m-%dT%H:%M:%S")
                modified = datetime.strptime(row['modified'], "%Y-%m-%dT%H:%M:%S")
                basename = row['basename']
                extension = row['extension']
                type_ = row['type']
                mode = row['mode']
                parent_path = row['parentpath']
                full_path = row['fullpath']
                file = File(fileid, name, bytes_, depth, accessed, modified, basename, extension, type_, mode,
                            parent_path, full_path)
                all_files.append(file)

        db = DbService()
        await db.initialize()

        print('all files: ', len(all_files))
        tasks = []

        for i, file_ in enumerate(all_files):
            tasks.append(create_task(db.upsert_file(file_)))
            if i % 500 == 0:
                print(f'import in {i / len(all_files) * 100:.1f}% done')
                await asyncio.gather(*tasks)
                tasks = []

        await asyncio.gather(*tasks)
        await db.heal_file_id()

        await sleep(1)


if __name__ == '__main__':
    db_file = 'data/database.sqlite'
    asyncio.run(do_import(db_file))
