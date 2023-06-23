import asyncpg
from dotenv import load_dotenv
from os import getenv
from asyncio import run
from model import *


load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')


class DbService:
    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5,
                                              server_settings={'search_path': SCHEMA})
        print(f'connected to [{URL}]')

    async def get_region(self, connection, region_id: UUID) -> Region | None:
        async with connection.transaction(isolation='serializable'):
            row = await connection.fetchrow('SELECT * FROM region WHERE region_id=$1', region_id)
        return Region(**dict(row)) if row else None

    async def upsert_region(self, region: Region) -> Region:
        async with self.pool.acquire() as connection:
            async with connection.transaction(isolation='serializable'):
                if region.region_id is None:
                    row = await connection.fetchrow("""INSERT INTO region(region_name) VALUES ($1) RETURNING *""",
                                                    region.region_name)
                elif await self.get_region(connection=connection, region_id=region.region_id) is None:
                    row = await connection.fetchrow(
                        """INSERT INTO region(region_id, region_name) VALUES($1, $2) RETURNING *""",
                        region.region_id, region.region_name)
                else:
                    # update
                    row = await connection.fetchrow(
                        """UPDATE region SET region_name=$2 WHERE region_id=$1 RETURNING *""",
                        region.region_id, region.region_name)
                return Region(**dict(row))

    async def get_election_type(self, connection, type_id: UUID) -> ElectionType | None:
        async with connection.transaction(isolation='serializable'):
            row = await connection.fetchrow('SELECT * FROM election_type WHERE type_id=$1', type_id)
        return ElectionType(**dict(row)) if row else None

    async def upsert_election_type(self, election_type: ElectionType) -> ElectionType:
        type_ = election_type
        async with self.pool.acquire() as connection:
            async with connection.transaction(isolation='serializable'):
                if type_.type_id is None:
                    row = await connection.fetchrow("""INSERT INTO election_type(type_name, no_of_choices) VALUES
                    ($1, $2) RETURNING *""", type_.type_name, type_.no_of_choices)
                elif await self.get_election_type(connection=connection, type_id=type_.type_id) is None:
                    row = await connection.fetchrow("""INSERT INTO election_type(type_id, type_name, no_of_choices)
                        VALUES($1, $2, $3) RETURNING *""", type_.type_id, type_.type_name, type_.no_of_choices)
                else:
                    # update
                    row = await connection.fetchrow("""UPDATE election_type SET type_name=$2, no_of_choices=$3 WHERE
                        type_id=$1 RETURNING *""", type_.type_id, type_.type_name, type_.no_of_choices)
                return ElectionType(**dict(row))

    async def get_choice(self, connection, choice_id: UUID) -> Choice | None:
        async with connection.transaction(isolation='serializable'):
            row = await connection.fetchrow('SELECT * FROM choice WHERE choice_id=$1', choice_id)
        return Choice(**dict(row)) if row else None

    async def upsert_choice(self, choice: Choice) -> Choice:
        async with self.pool.acquire() as connection:
            async with connection.transaction(isolation='serializable'):
                if choice.choice_id is None:
                    row = await connection.fetchrow("""INSERT INTO choice(choice_name, image) VALUES ($1, $2)
                        RETURNING *""", choice.choice_name, choice.image)
                elif await self.get_choice(connection=connection, choice_id=choice.choice_id) is None:
                    # insert
                    row = await connection.fetchrow("""INSERT INTO choice(choice_id, choice_name, image)
                        VALUES($1, $2, $3) RETURNING *""", choice.choice_id, choice.choice_name, choice.image)
                else:
                    # update
                    row = await connection.fetchrow("""UPDATE choice SET choice_name=$2, image=$3 WHERE
                        choice_id=$1 RETURNING *""", choice.choice_id, choice.choice_name, choice.image)
                return Choice(**dict(row))

    async def get_election(self, connection, election_id: UUID) -> Election | None:
        async with connection.transaction(isolation='serializable'):
            row = await connection.fetchrow('SELECT * FROM election WHERE election_id=$1', election_id)
        return Election(**dict(row)) if row else None

    async def upsert_election(self, election: Election) -> Election:
        async with self.pool.acquire() as connection:
            async with connection.transaction(isolation='serializable'):
                if election.election_id is None:
                    row = await connection.fetchrow("""INSERT INTO election(type_id, region_id, vote_start, vote_end)
                     VALUES ($1, $2, $3, $4) RETURNING *""", election.type_id, election.region_id,
                                                    election.vote_start, election.vote_end)
                elif await self.get_election(connection=connection, election_id=election.election_id) is None:
                    # insert
                    row = await connection.fetchrow("""INSERT INTO election(election_id, type_id, region_id, vote_start,
                    vote_end) VALUES ($1, $2, $3, $4, $5) RETURNING *""", election.election_id, election.type_id,
                                                    election.region_id, election.vote_start, election.vote_end)
                else:
                    # update
                    row = await connection.fetchrow("""UPDATE election_type SET type_id=$2, region_id=$3, vote_start=$4,
                    vote_end=#5 WHERE election_id=$1 RETURNING *""", election.election_id, election.type_id,
                                                    election.region_id, election.vote_start, election.vote_end)
                return Election(**dict(row))

    async def get_voter(self, connection, voter_id: UUID) -> Voter | None:
        async with connection.transaction(isolation='serializable'):
            row = await connection.fetchrow('SELECT * FROM voter WHERE voter_id=$1', voter_id)
        return Region(**dict(row)) if row else None

    async def upsert_voter(self, voter: Voter) -> Voter:
        async with self.pool.acquire() as connection:
            async with connection.transaction(isolation='serializable'):
                if voter.voter_id is None:
                    row = await connection.fetchrow("""INSERT INTO voter(voter_name) VALUES ($1) RETURNING *""",
                                                    voter.voter_name)
                elif await self.get_voter(connection=connection, voter_id=voter.voter_id) is None:
                    row = await connection.fetchrow(
                        """INSERT INTO voter(voter_id, voter_name) VALUES($1, $2) RETURNING *""",
                        voter.voter_id, voter.voter_name)
                else:
                    # update
                    row = await connection.fetchrow("""UPDATE voter SET voter_name=$2 WHERE voter_id=$1 RETURNING *""",
                                                    voter.voter_id, voter.voter_name)
                return Voter(**dict(row))

    async def add_choice_to_election(self, election_id: UUID, choice_id: UUID):
        async with self.pool.acquire() as connection:
            async with connection.transaction(isolation='serializable'):
                await connection.fetchrow("""INSERT INTO election_choices(election_id, choice_id) VALUES ($1, $2)""",
                                          election_id, choice_id)
                print('Added choice {} to election {}'.format(choice_id, election_id))

    async def view_choices(self, election_id: UUID) -> list[Choice]:
        async with self.pool.acquire() as connection:
            async with connection.transaction(isolation='serializable'):
                rows = await connection.fetch("""SELECT choice.* FROM choice JOIN election_choices ec ON
                            choice.choice_id = ec.choice_id WHERE election_id = $1;""", election_id)
        return [Choice(**dict(row)) for row in rows]

    async def add_voter_to_election(self, voter_id: UUID, election_id: UUID):
        async with self.pool.acquire() as connection:
            async with connection.transaction(isolation='serializable'):
                await connection.fetchrow("""INSERT INTO voter_elections(voter_id, election_id) VALUES ($1, $2)""",
                                          voter_id, election_id)
                print('Added voter {} to election {}'.format(voter_id, election_id))
    async def is_voter_assigned_to_election(self, connection, voter_id: UUID, election_id: UUID) -> bool:
        ans = await connection.fetchval("""SELECT EXISTS(SELECT 1 FROM voter_elections WHERE
                    voter_id=$1 AND election_id=$2);""", voter_id, election_id)
        return ans


    async def generate_token_for_voter(self, voter_id: UUID, election_id: UUID):
        async with self.pool.acquire() as connection:
            async with connection.transaction(isolation='serializable'):
                if not await self.is_voter_assigned_to_election(connection=connection, voter_id=voter_id,
                        election_id=election_id): raise AccessDenied('Voter is not assigned to these elections.')
                await connection.fetchrow("""DELETE FROM voter_elections WHERE voter_id=$1 AND election_id=$2""",
                                          voter_id, election_id)
                row = await connection.fetchrow("""INSERT INTO token(election_id) VALUES ($1) RETURNING *""",
                                                election_id)
                token = Token(**dict(row))
                return token

    async def is_token_valid(self, connection, token_id: UUID, election_id: UUID) -> bool:
        ans = await connection.fetchval("""SELECT EXISTS(SELECT 1 FROM token WHERE token_id=$1
                    AND election_id=$2)""", token_id, election_id)
        return ans

    async def get_number_of_choices(self, connection, election_id: UUID) -> int:
        ans = await connection.fetchval("""SELECT no_of_choices FROM election_type JOIN election e ON
                    election_type.type_id = e.type_id WHERE election_id = $1;""", election_id)
        return ans

    async def get_election_dates(self, connection, election_id: UUID) -> tuple[datetime, datetime]:
        dates = await connection.fetchrow("""SELECT vote_start, vote_end FROM election WHERE election_id=$1""",
                                          election_id)
        return dates

    async def cast_vote(self, token_id: UUID, election_id: UUID, votes: list[UUID]):
        async with self.pool.acquire() as connection:
            async with connection.transaction(isolation='serializable'):
                if not await self.is_token_valid(connection=connection, token_id=token_id, election_id=election_id):
                    raise AccessDenied('Voter has no token for these elections.')
                if await self.get_number_of_choices(connection=connection, election_id=election_id) != len(votes):
                    raise InvalidVote('This vote is invalid (incorrect number of choices).')
                vote_start, vote_end = await self.get_election_dates(connection=connection, election_id=election_id)
                now = datetime.now()
                if now > vote_end or now < vote_start:
                    raise AccessDenied('Time for voting has passed.')
                choices = {choice.choice_id for choice in await self.view_choices(election_id)}
                for vote in votes:
                    if not isinstance(vote, UUID):
                        raise InvalidVote('This vote is invalid (incorrect id).')
                    if vote not in choices:
                        raise InvalidVote('This vote is invalid (choice not listed).')
                await connection.fetchrow("""DELETE FROM token WHERE token_id=$1""", token_id)
                for vote in votes:
                    await connection.fetchrow("""INSERT INTO election_votes(election_id, choice_id) VALUES ($1, $2)""",
                                              election_id, vote)
                print('Vote {} casted for election {}'.format(votes, election_id))


async def main():
    db = DbService()
    await db.initialize()

    chiayi = await db.upsert_region(Region(region_id=None, region_name='Chiayi'))
    miaoli = await db.upsert_region(Region(region_id=None, region_name='Miaoli'))
    print(chiayi)
    print(miaoli)

    mayor = await db.upsert_election_type(ElectionType(type_id=None, type_name='Mayor', no_of_choices=1))
    council = await db.upsert_election_type(ElectionType(type_id=None, type_name='Council', no_of_choices=1))
    print(mayor)
    print(council)

    mayor_election = await db.upsert_election(Election(election_id=None, type_id=mayor.type_id,
        region_id=chiayi.region_id, vote_start=datetime(2023, 6, 24, 10), vote_end=datetime(2023, 6, 25, 8, 15)))
    council_election = await db.upsert_election(Election(election_id=None, type_id=council.type_id,
        region_id=miaoli.region_id, vote_start=datetime(2023, 6, 24, 8, 15), vote_end=datetime(2023, 6, 24, 17)))
    print(mayor_election)
    print(council_election)

    zhang_san = await db.upsert_choice(Choice(choice_id=None, choice_name='Zhang San', image='zhang_san.png'))
    li_si = await db.upsert_choice(Choice(choice_id=None, choice_name='Li Si', image='li_si.png'))
    print(zhang_san)
    print(li_si)

    wang_wu = await db.upsert_choice(Choice(choice_id=None, choice_name='Wang Wu', image='wang_wu.png'))
    lu_er = await db.upsert_choice(Choice(choice_id=None, choice_name='Lu Er', image='lu_er.png'))
    print(wang_wu)
    print(lu_er)

    await db.add_choice_to_election(election_id=mayor_election.election_id, choice_id=zhang_san.choice_id)
    await db.add_choice_to_election(election_id=mayor_election.election_id, choice_id=wang_wu.choice_id)
    await db.add_choice_to_election(election_id=council_election.election_id, choice_id=li_si.choice_id)
    await db.add_choice_to_election(election_id=council_election.election_id, choice_id=lu_er.choice_id)

    zhao_liu = await db.upsert_voter(Voter(voter_id=None, voter_name='Zhao Liu'))
    sun_qi = await db.upsert_voter(Voter(voter_id=None, voter_name='Sun Qi'))
    wang_ermazi = await db.upsert_voter(Voter(voter_id=None, voter_name='Wang Ermazi'))
    print(zhao_liu)
    print(sun_qi)
    print(wang_ermazi)

    await db.add_voter_to_election(voter_id=zhao_liu.voter_id, election_id=mayor_election.election_id)
    await db.add_voter_to_election(voter_id=sun_qi.voter_id, election_id=mayor_election.election_id)
    await db.add_voter_to_election(voter_id=sun_qi.voter_id, election_id=council_election.election_id)
    await db.add_voter_to_election(voter_id=wang_ermazi.voter_id, election_id=council_election.election_id)

    zhao_token = await db.generate_token_for_voter(voter_id=zhao_liu.voter_id, election_id=mayor_election.election_id)
    sun_token_ma = await db.generate_token_for_voter(voter_id=sun_qi.voter_id, election_id=mayor_election.election_id)
    sun_token_co = await db.generate_token_for_voter(voter_id=sun_qi.voter_id, election_id=council_election.election_id)
    wang_token = await db.generate_token_for_voter(voter_id=wang_ermazi.voter_id, election_id=council_election.election_id)
    print(zhao_token)
    print(sun_token_ma)
    print(sun_token_co)
    print(wang_token)

    choices_mayor = await db.view_choices(election_id=mayor_election.election_id)
    choices_council = await db.view_choices(election_id=council_election.election_id)
    print(choices_mayor)
    print(choices_council)

    await db.cast_vote(token_id=zhao_token.token_id, election_id=mayor_election.election_id,
                       votes=[zhang_san.choice_id])
    await db.cast_vote(token_id=sun_token_ma.token_id, election_id=mayor_election.election_id,
                       votes=[wang_wu.choice_id])
    await db.cast_vote(token_id=sun_token_co.token_id, election_id=council_election.election_id,
                       votes=[li_si.choice_id])
    await db.cast_vote(token_id=wang_token.token_id, election_id=council_election.election_id,
                       votes=[lu_er.choice_id])

if __name__ == '__main__':
    run(main())
