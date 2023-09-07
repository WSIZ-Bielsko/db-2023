import unittest
from asyncio import gather, create_task
from unittest import IsolatedAsyncioTestCase
from db import *


class Test(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        print('setup')
        self.db = DbService()
        self.uid1 = uuid4()
        self.eid1 = uuid4()

        await self.db.initialize()

    async def asyncTearDown(self):
        await self.db.test_cleanup()

    async def test_can_create_user(self):
        user = await self.db.create_user(User(self.uid1, 'xi'))

    async def test_can_create_election(self):
        election = await self.db.create_election(Election(self.eid1, 'e1'))

    async def test_can_register_for_election(self):
        u = await self.db.create_user(User(self.uid1, 'xi'))
        e = await self.db.create_election(Election(self.eid1, 'e1'))

        token = (await self.db.register_for_election(e.eid, u.uid)).tokenid
        tokens = await self.db.test_get_all_tokens()
        tokens = [t.tokenid for t in tokens]

        self.assertIsNotNone(token)
        self.assertTrue(token in tokens)

    async def test_can_vote_in_election(self):
        u = await self.db.create_user(User(self.uid1, 'xi'))
        e = await self.db.create_election(Election(self.eid1, 'e1'))

        token = (await self.db.register_for_election(e.eid, u.uid)).tokenid
        await self.db.vote(token, 17)
        votes = await self.db.get_all_votes(e.eid)

        self.assertEqual(len(votes), 1)

    async def test_cannot_get_many_tokens_for_user(self):
        u = await self.db.create_user(User(self.uid1, 'xi'))
        e = await self.db.create_election(Election(self.eid1, 'e1'))

        tasks = []
        N = 300
        errors = 0
        for i in range(N):
            tasks.append(create_task(self.db.register_for_election(self.eid1, self.uid1)))

        tokens = set()
        for t in tasks:
            try:
                # no error
                g = await t
                tokens.add(g.tokenid)
            except VotingError as e:
                # error
                errors += 1

        self.assertEqual(errors, N - 1)
        self.assertEqual(len(tokens), 1)

    async def test_token_can_vote_exactly_once(self):
        u = await self.db.create_user(User(self.uid1, 'xi'))
        e = await self.db.create_election(Election(self.eid1, 'e1'))

        N = 30

        token = await self.db.register_for_election(self.eid1, self.uid1)

        tasks = []
        for i in range(N):
            tasks.append(create_task(self.db.vote(token.tokenid, 3)))

        errors = 0
        for t in tasks:
            try:
                # no error
                g = await t
            except VotingError as e:
                # error
                errors += 1

        votes = await self.db.get_all_votes(self.eid1)

        self.assertEqual(errors, N - 1)
        self.assertEqual(len(votes), 1)

        # assert exactly one vote in table votes
        # assert len(self.db.get_votes_by_eid(self.eid1)) == 1


if __name__ == "__main__":
    unittest.main()
