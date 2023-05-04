from db_services import DbService
from functions import *
from model import *
from asyncio import *


async def createActors():
    db = DbService()
    await db.initialize()

    cast = get_cast()
    actors = get_actors_of_movie(cast)
    actors = [Actor(*a) for a in actors]

    for a, actor in enumerate(actors):
        await db.upsert_actor(actor)
        if a % 100 == 0:
            print(f'import actors in {a / len(actors) * 100:.1f}% done')

    await sleep(1)


if __name__ == "__main__":
    run(createActors())
