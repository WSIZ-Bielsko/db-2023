from aiosqlite import connect
from asyncio import run
from model import File
from datetime import datetime


class SQLite:
    async def initialize(self):
        self.connection = await connect('database.sqlite')
        print('Connected!')

    async def get_files(self, limit=500) -> list[File]:
        rows = await self.connection.execute_fetchall('select * from files order by basename limit $1', [limit])
        return [await fix_file_object(File(*r)) for r in rows]

    async def get_file(self, file_id: int) -> File | None:
        row = await self.connection.execute_fetchall('select * from files where fileid = $1', [file_id])
        return await fix_file_object(File(*row[0])) if len(row) > 0 else None


async def fix_file_object(file: File) -> File:
    new_file = file
    pattern = '%Y-%m-%dT%H:%M:%S'
    new_file.modified = datetime.strptime(file.modified, pattern)
    new_file.accessed = datetime.strptime(file.accessed, pattern)
    return new_file


async def main_():
    sqlite = SQLite()
    await sqlite.initialize()
    files = await sqlite.get_files()
    file = await sqlite.get_file(2023)
    print(files[111])
    print(file)

if __name__ == '__main__':
    run(main_())
