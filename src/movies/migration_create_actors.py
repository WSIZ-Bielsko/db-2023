from asyncio import run

from src.movies.analysis_tools import get_casts, get_actors
from src.movies.db_service import DbService
from src.movies.model import Actor


async def create_actors():
    db = DbService()
    await db.initialize()
    # await db.upsert_actor(Actor(1, 'Kadabra!'))

    casts_ = get_casts()
    actors = get_actors(casts_)
    actors = [Actor(*a) for a in actors]

    print(f'all actors: {len(actors)}')
    for a in actors:
        await db.upsert_actor(a)

if __name__ == '__main__':
    run(create_actors())
