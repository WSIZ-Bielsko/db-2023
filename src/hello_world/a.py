from asyncio import run, sleep

import asyncpg
from dotenv import load_dotenv
from os import getenv

from model import User

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')


class DbService:

    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5,
                                              server_settings={'search_path': SCHEMA})

        print('connected!')

    async def get_users(self, offset=0, limit=500) -> list[User]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from users order by username offset $1 limit $2', offset, limit)
        return [User(**dict(r)) for r in rows]

    async def upsert(self, user: User) -> User:
        # if user.uid==None -- new user -- insert; else update user with given user.uid
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow("insert into users(username, password) VALUES ($1, $2) returning *",
                                            user.username, user.password)
        return User(**dict(row))


async def main():
    db = DbService()
    await db.initialize()  # tu łączymy się z bazą danych
    users = await db.get_users()  # tu pobieramy dane z bazy danych
    print(users)
    await sleep(1)


if __name__ == '__main__':
    run(main())
