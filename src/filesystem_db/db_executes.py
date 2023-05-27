import asyncio

import aiosqlite    # pip install aiosqlite


async def doit():
    async with aiosqlite.connect('data/database.sqlite') as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM files') as cursor:
            async for row in cursor:
                fileid = row['fileid']
                name = row['name']
                modified = row['modified']
                print(f'{fileid=}, {name=}, {modified=}')

        # await db.execute('INSERT INTO foo some_table')
        # assert db.total_changes > 0


if __name__ == '__main__':
    asyncio.run(doit())