import unittest
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
        print('teardown')

    async def test_can_create_user(self):
        user = await self.db.create_user(User(self.uid1, 'xi'))
        await self.db.delete_user(user.uid)

    # todo: dodać test tworzący i usuwający election

    # todo:  dodać test w którym user z uid1 rejestruje się do wyborów eid1, czyli test do db.register_for_election


if __name__ == "__main__":
    unittest.main()
