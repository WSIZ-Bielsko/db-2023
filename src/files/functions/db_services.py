from asyncio import *
import asyncpg
from dotenv import *
from os import *

from model import *

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')


class DbService:

    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5, min_size=15, max_size=20,
                                              server_settings={'search_path': SCHEMA})

        print('connected!')

    async def get_files(self, offset=0, limit=500) -> list[File]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from files order by name offset $1 limit $2', offset, limit)
        return [File(**dict(r)) for r in rows]

    async def get_file(self, file_id: int) -> File | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from files where file_id=$1', file_id)
        return File(**dict(row)) if row else None

    async def upsert_file(self, f: File) -> File:
        # insert & generate file_id
        if f.file_id is None:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""insert into files(
                name, bytes, depth, accessed, modified, basename, extension, type, mode, parent_path, full_path
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) returning *""",
                                                f.name, f.bytes, f.depth, f.accessed, f.modified, f.basename,
                                                f.extension, f.type, f.mode,
                                                f.parent_path, f.full_path)
        elif await self.get_file(f.file_id) is None:
            # insert with external file_id
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""insert into files(
                file_id, name, bytes, depth, accessed, modified, basename, extension, type, mode, parent_path, full_path
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12) returning *""",
                                                f.file_id, f.name, f.bytes, f.depth, f.accessed, f.modified, f.basename,
                                                f.extension, f.type, f.mode,
                                                f.parent_path, f.full_path)
        else:
            async with self.pool.acquire() as connection:
                # update
                row = await connection.fetchrow("""insert into files(
                file_id, name, bytes, depth, accessed, modified, basename, extension, type, mode, parent_path, full_path
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12) returning *""",
                                                f.file_id, f.name, f.bytes, f.depth, f.accessed, f.modified, f.basename,
                                                f.extension, f.type, f.mode,
                                                f.parent_path, f.full_path)

        return File(**dict(row))


async def main_():
    db = DbService()
    await db.initialize()


if __name__ == '__main__':
    run(main_())
