from asyncio import run
import asyncpg
from dotenv import load_dotenv
from os import getenv
from model import File

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')


class DbService:

    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5,
                                              server_settings={'search_path': SCHEMA})

    async def get_files(self, offset=0, limit=500) -> list[File]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from files order by name offset $1 limit $2', offset, limit)
        return [File(**dict(r)) for r in rows]

    async def get_file(self, file_id: int) -> File | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from files where file_id=$1', file_id)
        return File(**dict(row)) if row else None

    async def upsert_file(self, file: File) -> File:
        if file.file_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""insert into files(name, bytes, depth, accessed, modified, basename,
                extension, type, mode, parent_path, full_path) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                returning *""", file.name, file.bytes, file.depth, file.accessed, file.modified, file.basename,
                file.extension, file.type, file.mode, file.parent_path, file.full_path)
                await connection.fetchrow("select setval('files_file_id_seq', (select max(file_id) from files))")
        elif await self.get_file(file.file_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""insert into files(file_id, name, bytes, depth, accessed, modified,
                basename, extension, type, mode, parent_path, full_path) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9,
                $10, $11, $12) returning *""", file.file_id, file.name, file.bytes, file.depth, file.accessed,
                file.modified, file.basename, file.extension, file.type, file.mode, file.parent_path, file.full_path)
                await connection.fetchrow("select setval('files_file_id_seq', (select max(file_id) from files))")
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update files set name=$2, bytes=$3, depth=$4, accessed=$5,
                modified=$6, basename=$7, extension=$8, type=$9, mode=$10, parent_path=$11, full_path=$12 where
                file_id=$1 returning *""", file.file_id, file.name, file.bytes, file.depth, file.accessed,
                file.modified, file.basename, file.extension, file.type, file.mode, file.parent_path, file.full_path)
        return File(**dict(row))


async def main_():
    from datetime import datetime
    db = DbService()
    await db.initialize()
    await db.upsert_file(File(1, 'test.py', 1024, 1, datetime(2023, 5, 27, 10, 5, 36), datetime(2023, 2, 15, 22, 45, 1),
                              'test', '.py', 'f', '-rwxrw-r--', 'files/', 'files/test.py'))


if __name__ == '__main__':
    run(main_())
