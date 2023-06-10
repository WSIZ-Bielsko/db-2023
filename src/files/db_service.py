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
                parent = await connection.fetchrow("select * from files where full_path = $1", file.parent_path)
                if parent is None: raise FileNotFoundError(f'Parent "{file.parent_path}" does not exist')
                row = await connection.fetchrow("""insert into files(name, bytes, depth, accessed, modified, basename,
                extension, type, mode, parent_path, full_path) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                returning *""", file.name, file.bytes, file.depth, file.accessed, file.modified, file.basename,
                file.extension, file.type, file.mode, file.parent_path, file.full_path)
                await connection.fetchrow("select setval('files_file_id_seq', (select max(file_id) from files))")
        elif await self.get_file(file.file_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                parent = await connection.fetchrow("select * from files where full_path = $1", file.parent_path)
                if parent is None: raise FileNotFoundError('Such parent does not exist')
                row = await connection.fetchrow("""insert into files(file_id, name, bytes, depth, accessed, modified,
                basename, extension, type, mode, parent_path, full_path) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9,
                $10, $11, $12) returning *""", file.file_id, file.name, file.bytes, file.depth, file.accessed,
                file.modified, file.basename, file.extension, file.type, file.mode, file.parent_path, file.full_path)
                await connection.fetchrow("select setval('files_file_id_seq', (select max(file_id) from files))")
        else:
            # update
            async with self.pool.acquire() as connection:
                parent = await connection.fetchrow("select * from files where full_path = $1", file.parent_path)
                if parent is None: raise FileNotFoundError('Such parent does not exist')
                row = await connection.fetchrow("""update files set name=$2, bytes=$3, depth=$4, accessed=$5,
                modified=$6, basename=$7, extension=$8, type=$9, mode=$10, parent_path=$11, full_path=$12 where
                file_id=$1 returning *""", file.file_id, file.name, file.bytes, file.depth, file.accessed,
                file.modified, file.basename, file.extension, file.type, file.mode, file.parent_path, file.full_path)
        return File(**dict(row))

    async def create_file(self, file: File) -> File:
        if file.type != 'f': raise FileNotFoundError('This is not a file')
        return await self.upsert_file(file)

    async def create_dir(self, directory: File) -> File:
        if directory.type != 'd': raise NotADirectoryError('This is not a directory')
        return await self.upsert_file(directory)

    async def rm_file(self, file_id: int) -> File | None:
        async with self.pool.acquire() as connection:
            file = await connection.fetchrow('delete from files where file_id=$1 returning *', file_id)
        return File(**dict(file)) if file else None

    async def rm_dir(self, file_id: int) -> File | None:
        async with self.pool.acquire() as connection:
            parent = await connection.fetchrow('delete from files where file_id=$1 returning *', file_id)
            if parent is None: return parent
            await connection.fetchrow('delete from files where parent_path=$1', parent[-1])
        return File(**dict(parent))


async def main_():
    from datetime import datetime
    db = DbService()
    await db.initialize()

    await db.create_dir(File(None, 'test', 2048, 1, datetime(2023, 5, 27, 10, 5, 36), datetime(2023, 2, 15, 22, 45, 1),
    'user', '', 'd', '-rwxrw-r--', '/Users/peterdalloz/gutenberg/', '/Users/peterdalloz/gutenberg/test/'))
    await db.create_file(File(None, 'test.py', 1024, 2, datetime(2023, 5, 27, 10, 5, 36), datetime(2023, 2, 15, 22, 45, 1),
    'test', '.py', 'f', '-rwxrw-r--', '/Users/peterdalloz/gutenberg/test/', '/Users/peterdalloz/gutenberg/test/test.py'))
    await db.create_file(File(None, 'test.sql', 1024, 2, datetime(2023, 5, 27, 10, 5, 36), datetime(2023, 2, 15, 22, 45, 1),
    'test', '.sql', 'f', '-rwxrw-r--', '/Users/peterdalloz/gutenberg/test/', '/Users/peterdalloz/gutenberg/test/test.sql'))

    await db.rm_file(218723)
    await db.rm_dir(218722)

if __name__ == '__main__':
    run(main_())
