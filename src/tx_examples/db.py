import asyncio
import uuid
from asyncio import run, create_task
from datetime import datetime
from random import choice

import asyncpg
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
            rows = await connection.fetch('select * from accounts order by account_name offset $1 limit $2',
                                          offset, limit)
        return [Account(**dict(r)) for r in rows]

    async def get_account(self, account_id: uuid) -> Account | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from accounts where account_id=$1', account_id)
        return Account(**dict(row)) if row else None

    async def get_account_by_name(self, account_name: str) -> Account | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from accounts where account_name=$1', account_name)
        return Account(**dict(row)) if row else None

    async def upsert_account(self, account: Account) -> Account:
        a = account

        if a.account_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into accounts(account_name, balance) 
                        VALUES ($1, $2) returning *""", a.account_name, a.balance)
                return Account(**dict(row))

        elif await self.get_account(a.account_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into accounts(account_id, account_name, balance) values($1,$2,$3) returning *""",
                    a.account_id, a.account_name, a.balance)
        else:
            # update
            async with self.pool.acquire() as connection:
                # async with connection.transaction(isolation='serializable') as tx:
                row = await connection.fetchrow("""
                                   update accounts set account_name=$2, balance=$3 where account_id=$1 returning *""",
                                                a.account_id, a.account_name, a.balance)
        return Account(**dict(row))

    async def increment_amount_on_account(self, acc: Account, update_id: int, rollback_all=False):
        for retry in range(30):
            async with self.pool.acquire() as con:
                try:
                    # other levels: 'read_committed', 'repeatable_read', 'serializable'
                    async with con.transaction(isolation='serializable'):
                        # get current amount
                        balance = await con.fetchval('select balance from accounts where account_id=$1', acc.account_id)

                        # just a delay - for testing
                        # await sleep(0.02 + 0.1 * random())

                        # update the account
                        await con.execute('update accounts set balance=$2 where account_id=$1',
                                          acc.account_id, balance + 1)

                        if rollback_all:
                            raise RuntimeError('just a dry run...')

                except asyncpg.exceptions.SerializationError:
                    print(f'retry #{retry} by id={update_id}')
                    continue
                except RuntimeError:
                    print('meh...dry run')
                    break
                print(f'update id={update_id} -> to {balance + 1}')
                break


def ts():
    return datetime.now().timestamp()


async def main():
    db = DbService()
    await db.initialize()
    accounts = await db.get_accounts()
    account = await db.get_account_by_name('wu')
    account.amount = 0
    await db.upsert_account(account)
    print(account)
    t = []
    st = ts()
    for update_id in range(30):
        random_account = choice(accounts)  # account
        t.append(create_task(db.increment_amount_on_account(random_account, update_id, rollback_all=True)))
        # await db.update_amount(account, update_id)
    await asyncio.gather(*t)
    en = ts()
    print(await db.get_account(account.account_id))  # amount=100?
    print(f'full operation duration: {en-st:.3}s')


if __name__ == '__main__':
    run(main())
