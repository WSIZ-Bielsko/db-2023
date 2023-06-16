import asyncio
import uuid
from asyncio import run, sleep, create_task

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
                async with connection.transaction(isolation='serializable') as tx:
                    row = await connection.fetchrow("""
                                   update accounts set name=$2, amount=$3 where id=$1 returning *""",
                                                    a.id, a.name, a.amount)
        return Account(**dict(row))

    async def update_amount(self, acc: Account, extra_amount: int, update_id: int):
        for retry in range(10):
            try:
                current = (await self.get_account(acc.id)).amount
                print(f'{update_id=}, current={current}')
                acc.amount = current + extra_amount
                new_acc = await self.upsert_account(acc)
            except asyncpg.exceptions.SerializationError as f:
                print(f'retry #{retry}')
                continue
            print(f'update id={update_id} -> to {new_acc}')
            break


async def main():
    db = DbService()
    await db.initialize()
    # accounts = await db.get_accounts()
    ac = await db.get_account('c5097dba-ead5-4abd-aba1-b65db4e16f37')
    ac.amount = 0
    await db.upsert_account(ac)
    print(ac)
    t = []
    for update_id in range(100):
        t.append(create_task(db.update_amount(ac, 1, update_id)))
        # await db.update_amount(ac, 1)
    await asyncio.gather(*t)
    print(await db.get_account(ac.id))  #amount=100?


if __name__ == '__main__':
    run(main())
