from asyncpg import create_pool
from asyncpg.exceptions import SerializationError
from dotenv import load_dotenv
from os import getenv
from asyncio import run
from model import *

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')
TRANSACTION_MODE = 'serializable'  # 'read_committed'


class DbService:
    pool = None

    async def initialize(self):
        self.pool = await create_pool(URL, timeout=30, command_timeout=5, server_settings={'search_path': SCHEMA})
        await log(f'connected to [{URL}]')

    @staticmethod
    async def get_region(connection, region_id: UUID) -> Region | None:
        async with connection.transaction(isolation=TRANSACTION_MODE):
            row = await connection.fetchrow('SELECT * FROM region WHERE region_id=$1', region_id)
        return Region(**dict(row)) if row else None

    async def upsert_region(self, region: Region) -> Region:
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        if region.region_id is None:
                            row = await connection.fetchrow("""INSERT INTO region(region_name) VALUES ($1) RETURNING 
                            *""", region.region_name)
                        elif await self.get_region(connection=connection, region_id=region.region_id) is None:
                            row = await connection.fetchrow("""INSERT INTO region(region_id, region_name) VALUES($1, 
                            $2) RETURNING *""", region.region_id, region.region_name)
                        else:
                            # update
                            row = await connection.fetchrow("""UPDATE region SET region_name=$2 WHERE region_id=$1 
                            RETURNING *""", region.region_id, region.region_name)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Added region {}'.format(row))
                return Region(**dict(row))

    async def delete_region(self, region_id: UUID):
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        await connection.fetchrow('DELETE FROM region WHERE region_id=$1', region_id)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Deleted region {}'.format(region_id))
                break

    @staticmethod
    async def get_election_type(connection, type_id: UUID) -> ElectionType | None:
        async with connection.transaction(isolation=TRANSACTION_MODE):
            row = await connection.fetchrow('SELECT * FROM election_type WHERE type_id=$1', type_id)
        return ElectionType(**dict(row)) if row else None

    async def upsert_election_type(self, election_type: ElectionType) -> ElectionType:
        type_ = election_type
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        if type_.type_id is None:
                            row = await connection.fetchrow("""INSERT INTO election_type(type_name, no_of_choices) 
                            VALUES ($1, $2) RETURNING *""", type_.type_name, type_.no_of_choices)
                        elif await self.get_election_type(connection=connection, type_id=type_.type_id) is None:
                            row = await connection.fetchrow("""INSERT INTO election_type(type_id, type_name, 
                            no_of_choices) VALUES($1, $2, $3) RETURNING *""", type_.type_id, type_.type_name,
                                                            type_.no_of_choices)
                        else:
                            # update
                            row = await connection.fetchrow("""UPDATE election_type SET type_name=$2, 
                            no_of_choices=$3 WHERE type_id=$1 RETURNING *""", type_.type_id, type_.type_name,
                                                            type_.no_of_choices)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Added election type {}'.format(row))
                return ElectionType(**dict(row))

    async def delete_election_type(self, type_id: UUID):
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        await connection.fetchrow('DELETE FROM election_type WHERE type_id=$1', type_id)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Deleted election type {}'.format(type_id))
                break

    @staticmethod
    async def get_choice(connection, choice_id: UUID) -> Choice | None:
        async with connection.transaction(isolation=TRANSACTION_MODE):
            row = await connection.fetchrow('SELECT * FROM choice WHERE choice_id=$1', choice_id)
        return Choice(**dict(row)) if row else None

    async def upsert_choice(self, choice: Choice) -> Choice:
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        if choice.choice_id is None:
                            row = await connection.fetchrow("""INSERT INTO choice(choice_name, image) VALUES ($1, 
                            $2) RETURNING *""", choice.choice_name, choice.image)
                        elif await self.get_choice(connection=connection, choice_id=choice.choice_id) is None:
                            # insert
                            row = await connection.fetchrow("""INSERT INTO choice(choice_id, choice_name, image) 
                            VALUES($1, $2, $3) RETURNING *""", choice.choice_id, choice.choice_name, choice.image)
                        else:
                            # update
                            row = await connection.fetchrow("""UPDATE choice SET choice_name=$2, image=$3 WHERE 
                            choice_id=$1 RETURNING *""", choice.choice_id, choice.choice_name, choice.image)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Added choice {}'.format(row))
                return Choice(**dict(row))

    async def delete_choice(self, choice_id: UUID):
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        await connection.fetchrow('DELETE FROM choice WHERE choice_id=$1', choice_id)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Deleted choice {}'.format(choice_id))
                break

    @staticmethod
    async def get_election(connection, election_id: UUID) -> Election | None:
        async with connection.transaction(isolation=TRANSACTION_MODE):
            row = await connection.fetchrow('SELECT * FROM election WHERE election_id=$1', election_id)
        return Election(**dict(row)) if row else None

    async def upsert_election(self, election: Election) -> Election:
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        if election.election_id is None:
                            row = await connection.fetchrow("""INSERT INTO election(type_id, region_id, vote_start, 
                            vote_end) VALUES ($1, $2, $3, $4) RETURNING *""", election.type_id, election.region_id,
                                                            election.vote_start, election.vote_end)
                        elif await self.get_election(connection=connection, election_id=election.election_id) is None:
                            # insert
                            row = await connection.fetchrow("""INSERT INTO election(election_id, type_id, region_id, 
                            vote_start, vote_end) VALUES ($1, $2, $3, $4, $5) RETURNING *""", election.election_id,
                                                            election.type_id, election.region_id,
                                                            election.vote_start, election.vote_end)
                        else:
                            # update
                            row = await connection.fetchrow("""UPDATE election SET type_id=$2, region_id=$3, 
                            vote_start=$4, vote_end=$5 WHERE election_id=$1 RETURNING *""", election.election_id,
                                                            election.type_id, election.region_id, election.vote_start,
                                                            election.vote_end)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Added election {}'.format(row))
                return Election(**dict(row))

    async def delete_election(self, election_id: UUID):
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        await connection.fetchrow('DELETE FROM election WHERE election_id=$1', election_id)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Deleted election {}'.format(election_id))
                break

    @staticmethod
    async def get_voter(connection, voter_id: UUID) -> Voter | None:
        async with connection.transaction(isolation=TRANSACTION_MODE):
            row = await connection.fetchrow('SELECT * FROM voter WHERE voter_id=$1', voter_id)
        return Region(**dict(row)) if row else None

    async def upsert_voter(self, voter: Voter) -> Voter:
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        if voter.voter_id is None:
                            row = await connection.fetchrow("""INSERT INTO voter(voter_name) VALUES ($1) RETURNING *""",
                                                            voter.voter_name)
                        elif await self.get_voter(connection=connection, voter_id=voter.voter_id) is None:
                            row = await connection.fetchrow("""INSERT INTO voter(voter_id, voter_name) VALUES($1, 
                            $2) RETURNING *""", voter.voter_id, voter.voter_name)
                        else:
                            # update
                            row = await connection.fetchrow("""UPDATE voter SET voter_name=$2 WHERE voter_id=$1 
                            RETURNING *""", voter.voter_id, voter.voter_name)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Added voter {}'.format(row))
                return Voter(**dict(row))

    async def delete_voter(self, voter_id: UUID):
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        await connection.fetchrow('DELETE FROM voter WHERE voter_id=$1', voter_id)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Deleted voter {}'.format(voter_id))
                break

    async def add_choice_to_election(self, election_id: UUID, choice_id: UUID):
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        await connection.fetchrow("""INSERT INTO election_choices(election_id, choice_id) VALUES ($1, 
                        $2) """, election_id, choice_id)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Added choice {} to election {}'.format(choice_id, election_id))
                break

    async def delete_choice_from_election(self, election_id: UUID, choice_id: UUID):
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        await connection.fetchrow("""DELETE FROM election_choices WHERE election_id=$1 AND 
                        choice_id=$2""", election_id, choice_id)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Deleted choice {} from election {}'.format(choice_id, election_id))
                break

    @staticmethod
    async def view_choices(connection, election_id: UUID) -> list[Choice]:
        for retry in range(10):
            try:
                async with connection.transaction(isolation=TRANSACTION_MODE):
                    rows = await connection.fetch("""SELECT choice.* FROM choice JOIN election_choices ec ON 
                    choice.choice_id = ec.choice_id WHERE election_id = $1;""", election_id)
            except SerializationError:
                await log(f'Retry #{retry}')
                continue
            return [Choice(**dict(row)) for row in rows]

    async def add_voter_to_election(self, voter_id: UUID, election_id: UUID):
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        await connection.fetchrow(
                            """INSERT INTO voter_elections(voter_id, election_id) VALUES ($1, $2)""", voter_id,
                            election_id)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Added voter {} to election {}'.format(voter_id, election_id))
                break

    @staticmethod
    async def delete_voter_from_election(connection, election_id: UUID, voter_id: UUID):
        for retry in range(10):
            try:
                async with connection.transaction(isolation=TRANSACTION_MODE):
                    await connection.fetchrow("""DELETE FROM voter_elections WHERE election_id=$1 AND voter_id=$2""",
                                              election_id, voter_id)
            except SerializationError:
                await log(f'Retry #{retry}')
                continue
            await log('Deleted voter {} from election {}'.format(voter_id, election_id))
            break

    @staticmethod
    async def is_voter_assigned_to_election(connection, voter_id: UUID, election_id: UUID) -> bool:
        ans = await connection.fetchval(
            """SELECT EXISTS(SELECT 1 FROM voter_elections WHERE voter_id=$1 AND election_id=$2);""", voter_id,
            election_id)
        return ans

    async def generate_token_for_voter(self, voter_id: UUID, election_id: UUID):
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        if not await self.is_voter_assigned_to_election(connection=connection, voter_id=voter_id,
                                                                        election_id=election_id):
                            raise AccessDenied('Voter is not assigned to these elections.')
                        await self.delete_voter_from_election(connection, election_id, voter_id)
                        row = await connection.fetchrow("""INSERT INTO token(election_id) VALUES ($1) RETURNING *""",
                                                        election_id)
                        token = Token(**dict(row))
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Generated token {}'.format(token))
                return token

    @staticmethod
    async def delete_token(connection, token_id: UUID):
        for retry in range(10):
            try:
                async with connection.transaction(isolation=TRANSACTION_MODE):
                    await connection.fetchrow("""DELETE FROM token WHERE token_id=$1""", token_id)
            except SerializationError:
                await log(f'Retry #{retry}')
                continue
            await log('Token {} deleted'.format(token_id))
            break

    @staticmethod
    async def is_token_valid(connection, token_id: UUID, election_id: UUID) -> bool:
        async with connection.transaction(isolation=TRANSACTION_MODE):
            ans = await connection.fetchval("""SELECT EXISTS(SELECT 1 FROM token WHERE token_id=$1 AND 
            election_id=$2)""", token_id, election_id)
            return ans

    @staticmethod
    async def get_number_of_choices(connection, election_id: UUID) -> int:
        async with connection.transaction(isolation=TRANSACTION_MODE):
            ans = await connection.fetchval("""SELECT no_of_choices FROM election_type JOIN election e ON 
            election_type.type_id = e.type_id WHERE election_id = $1;""", election_id)
            return ans

    @staticmethod
    async def get_election_dates(connection, election_id: UUID) -> tuple[datetime, datetime]:
        async with connection.transaction(isolation=TRANSACTION_MODE):
            dates = await connection.fetchrow("""SELECT vote_start, vote_end FROM election WHERE election_id=$1""",
                                              election_id)
            return dates

    async def vote_verification(self, connection, election_id: UUID, votes: list[UUID]):
        async with connection.transaction(isolation=TRANSACTION_MODE):
            if await self.get_number_of_choices(connection=connection, election_id=election_id) != len(votes):
                raise InvalidVote('This vote is invalid (incorrect number of choices).')
            vote_start, vote_end = await self.get_election_dates(connection=connection, election_id=election_id)
            now = datetime.now()
            if now > vote_end or now < vote_start:
                raise AccessDenied('It is not time for voting.')
            choices = {choice.choice_id for choice in await self.view_choices(connection=connection,
                                                                              election_id=election_id)}
            for vote in votes:
                if not isinstance(vote, UUID):
                    raise InvalidVote('This vote is invalid (incorrect id).')
                if vote not in choices:
                    raise InvalidVote('This vote is invalid (choice not listed).')

    async def cast_vote(self, token_id: UUID, election_id: UUID, votes: list[UUID]):
        for retry in range(10):
            async with self.pool.acquire() as connection:
                try:
                    async with connection.transaction(isolation=TRANSACTION_MODE):
                        if not await self.is_token_valid(connection=connection,
                                                         token_id=token_id, election_id=election_id):
                            raise AccessDenied('Voter has no token for these elections.')
                        await self.vote_verification(connection=connection, election_id=election_id, votes=votes)
                        await self.delete_token(connection, token_id)
                        for vote in votes:
                            await connection.fetchrow("""INSERT INTO election_votes(election_id, choice_id)
                            VALUES ($1, $2)""", election_id, vote)
                except SerializationError:
                    await log(f'Retry #{retry}')
                    continue
                await log('Vote {} casted for election {}'.format(votes, election_id))
                break


async def main():
    db = DbService()
    await db.initialize()

    taipei = await db.upsert_region(Region(None, 'Taipei'))
    mayor = await db.upsert_election_type(ElectionType(None, 'Mayor', 1))
    election = await db.upsert_election(
        Election(None, mayor.type_id, taipei.region_id, datetime(2023, 6, 30, 16, 15), datetime(2023, 7, 1, 17)))

    choice = await db.upsert_choice(Choice(None, 'Zhang San', 'zhang_san.png'))
    await db.add_choice_to_election(election.election_id, choice.choice_id)

    voter = await db.upsert_voter(Voter(None, 'Zhao Liu'))
    await db.add_voter_to_election(voter.voter_id, election.election_id)

    token = await db.generate_token_for_voter(voter.voter_id, election.election_id)
    await db.cast_vote(token.token_id, election.election_id, [choice.choice_id])

    await db.delete_voter(voter.voter_id)
    await db.delete_choice_from_election(election.election_id, choice.choice_id)
    await db.delete_choice(choice.choice_id)

    await db.delete_election(election.election_id)
    await db.delete_election_type(mayor.type_id)
    await db.delete_region(taipei.region_id)


async def log(message: str):
    print('[{}]: {}'.format(datetime.now(), message))


if __name__ == '__main__':
    run(main())
