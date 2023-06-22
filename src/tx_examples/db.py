import asyncio
import uuid
from asyncio import run, sleep, create_task
from datetime import datetime
from random import randint, random

import asyncpg
from asyncpg import SerializationError
from dotenv import load_dotenv
from os import getenv

from model import Account

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')


class DbService:

    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5,
                                              server_settings={'search_path': SCHEMA})

        print(f'connected to [{URL}]')

    async def get_accounts(self, offset=0, limit=500) -> list[Account]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from accounts order by name offset $1 limit $2', offset, limit)
        return [Account(**dict(r)) for r in rows]

    async def get_account(self, account_id: uuid) -> Account | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from accounts where id=$1', account_id)
        return Account(**dict(row)) if row else None

    async def get_account_by_name(self, account_name: str) -> Account | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from accounts where name=$1', account_name)
        return Account(**dict(row)) if row else None

    async def upsert_account(self, account: Account) -> Account:
        a = account

        if a.id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into accounts(name, amount) 
                        VALUES ($1, $2) returning *""", a.name, a.amount)
                return Account(**dict(row))

        elif await self.get_account(a.id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into accounts(id, name, amount) values($1,$2,$3) returning *""",
                    a.id, a.name, a.amount)
        else:
            # update
            async with self.pool.acquire() as connection:
                # async with connection.transaction(isolation='serializable') as tx:
                row = await connection.fetchrow("""
                                   update accounts set name=$2, amount=$3 where id=$1 returning *""",
                                                a.id, a.name, a.amount)
        return Account(**dict(row))

    async def update_amount(self, acc: Account, update_id: int):
        for retry in range(30):
            async with self.pool.acquire() as con:
                try:
                    # other levels: 'read_committed', 'repeatable_read', 'serializable'
                    async with con.transaction(isolation='repeatable_read') as tx:
                        # get current amount
                        amount = await con.fetchval('select amount from accounts where id=$1', acc.id)

                        # just a delay - for testing
                        # await sleep(0.02 + 0.1 * random())

                        # update the account
                        await con.execute('update accounts set amount=$2 where id=$1', acc.id, amount + 1)

                except asyncpg.exceptions.SerializationError as f:
                    print(f'retry #{retry} by id={update_id}')
                    continue
                print(f'update id={update_id} -> to {amount + 1}')
                break

def ts():
    return datetime.now().timestamp()

async def main():
    db = DbService()
    await db.initialize()
    account = await db.get_account_by_name('wu')
    account.amount = 0
    await db.upsert_account(account)
    print(account)
    t = []
    st = ts()
    for update_id in range(30):
        t.append(create_task(db.update_amount(account, update_id)))
        # await db.update_amount(account, update_id)
    await asyncio.gather(*t)
    en = ts()
    print(await db.get_account(account.id))  # amount=100?
    print(f'full operation duration: {en-st:.3}s')


if __name__ == '__main__':
    run(main())
