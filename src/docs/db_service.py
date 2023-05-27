from __future__ import annotations

from asyncio import run, sleep
from uuid import uuid4

import asyncpg
from dotenv import load_dotenv
from os import getenv

from model import *

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')


class DbService:

    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5, min_size=15, max_size=20,
                                              server_settings={'search_path': SCHEMA})

        print('connected!')

    # actors

    async def get_files(self, offset=0, limit=500) -> list[File]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from files order by name offset $1 limit $2', offset, limit)
        return [File(**dict(r)) for r in rows]

    async def get_file(self, fileid: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from files where fileid=$1', fileid)
        return File(**dict(row)) if row else None

    async def upsert_file(self, file: File) -> File:
        if file.fileid is None:
            # insert; `file` as no id assigned
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    "insert into files(name, bytes, depth, accessed, modified, basename, extension, type, mode, parentpath, fullpath) VALUES ($1,$2,$3,$4,$2,$6,$7,$8,$9,$10,$11) returning *",
                    file.name, file.bytes, file.depth, file.accessed, file.modified, file.basename, file.extension,
                    file.type, file.mode, file.parentpath, file.fullpath)

        elif await self.get_file(file.fileid) is None:
            # insert; `file` has id assigned externally
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    "insert into files(fileid, name, bytes, depth, accessed, modified, basename, extension, type, mode, parentpath, fullpath) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12) returning *",
                    file.fileid, file.name, file.bytes, file.depth, file.accessed, file.modified, file.basename,
                    file.extension, file.type, file.mode, file.parentpath, file.fullpath)

        else:
            # update; `file` with given id exists in db
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """update files set name=$2, bytes=$3, depth=$4, accessed=$5, modified=$6, basename=$7, extension=$8, type=$9, mode=$10, parentpath=$11, fullpath=$12 where fileid=$1 returning *""",
                    file.fileid, file.name, file.bytes, file.depth, file.accessed, file.modified, file.basename,
                    file.extension, file.type, file.mode, file.parentpath, file.fullpath)

        return File(**dict(row))

    async def update_serial(self):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow("""SELECT setval('files_fileid_seq',(SELECT MAX(fileid) FROM files))""")

    async def create_file(self, where: str, name: str, type: str = "", mode: str = "", bytes: int = 0):
        async with self.pool.acquire() as connection:
            onlyName = name.split(".")[0]
            extension = name.split(".")[1]
            fullpath = where + name
            currentDate = datetime.now()

            depth = 1

            row = await connection.fetchrow("""INSERT into files(name, parentpath, fullpath, modified, extension, type, mode, bytes, depth, basename) values($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) returning *""",
                                            name, where, fullpath, currentDate, extension, type, mode, bytes, depth, onlyName)