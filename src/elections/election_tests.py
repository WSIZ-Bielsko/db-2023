from asyncio import create_task, gather
from unittest import IsolatedAsyncioTestCase
from uuid import uuid4
from db_service import *


class Test(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        print('setup')
        self.db = DbService()
        self.voter_id, self.voter_name = uuid4(), 'xi'
        self.region_id, self.region_name = uuid4(), 'taipei'
        self.type_id, self.type_name = uuid4(), 'mayor'
        self.election_id, self.election_date = uuid4(), datetime(2023, 7, 1, 17)

        await self.db.initialize()

    async def asyncTearDown(self):
        await self.db.delete_voter(self.voter_id)
        await self.db.delete_election_type(self.type_id)
        await self.db.delete_region(self.region_id)
        await self.db.delete_election(self.election_id)
        print('teardown')

    async def test_can_create_user(self):
        voter = await self.db.upsert_voter(Voter(self.voter_id, self.voter_name))
        await self.db.delete_voter(voter.voter_id)

    async def test_can_create_region(self):
        region = await self.db.upsert_region(Region(self.region_id, self.region_name))
        await self.db.delete_region(region.region_id)

    async def test_can_create_election_type(self):
        election_type = await self.db.upsert_election_type(ElectionType(self.type_id, self.type_name, 1))
        await self.db.delete_election_type(election_type.type_id)

    async def test_can_create_election(self):
        await self.db.upsert_election_type(ElectionType(self.type_id, self.type_name, 1))
        await self.db.upsert_region(Region(self.region_id, self.region_name))
        election = await self.db.upsert_election(Election(self.election_id, self.type_id, self.region_id,
                                                          self.election_date, self.election_date))
        await self.db.delete_election(election.election_id)

    async def test_can_register_for_election(self):
        await self.db.upsert_voter(Voter(self.voter_id, self.voter_name))
        await self.db.upsert_election_type(ElectionType(self.type_id, self.type_name, 1))
        await self.db.upsert_region(Region(self.region_id, self.region_name))
        await self.db.upsert_election(Election(self.election_id, self.type_id, self.region_id,
                                               self.election_date, self.election_date))
        await self.db.add_voter_to_election(self.voter_id, self.election_id)
        async with self.db.pool.acquire() as connection:
            await self.db.is_voter_assigned_to_election(connection, self.voter_id, self.election_id)

    async def test_cannot_register_more_than_once(self):
        t = []
        for _ in range(10):
            t.append(create_task(self.test_can_register_for_election()))
        with self.assertRaises(AccessDenied):
            await gather(*t)


if __name__ == "__main__":
    main()
