import asyncio
import uuid
from asyncio import run, create_task
from datetime import datetime
from os import getenv
from random import choice

import asyncpg
from dotenv import load_dotenv

from model import *

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')




class DbService:

    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5,
                                              server_settings={'search_path': SCHEMA})

        print(f'connected to [{URL}]')

    async def create_user(self, user: User) -> User:
        pass

    async def delete_user(self, uid: uuid):
        pass

    async def create_election(self, user: User) -> User:
        pass

    async def delete_election(self, eid: uuid):
        pass


    async def register_for_election(self, eid: uuid, uid: uuid) -> uuid:
        """
        User with `uid` registers for election `eid`; raises VotingError if already voted, or
        `uid` or `eid` are invalid.

        Transactional.

        :param eid:
        :param uid:
        :return:
        """

    async def vote(self, tokenid: uuid, votevalue: int) -> uuid:
        """
        User with token `tokenid` votes in election. Appropriate row is created in Votes; token is removed.


        Transactional.

        :param eid:
        :param uid:
        :raises: VotingError if tokenid is invalid
        :return:
        """


def ts():
    return datetime.now().timestamp()


async def main():
    db = DbService()
    await db.initialize()


if __name__ == '__main__':
    run(main())
