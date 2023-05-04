from db_services import DbService
from functions import *
from asyncio import *


async def createCrew():
    db = DbService()
    await db.initialize()

    crew = get_crew()
    persons = get_crew_persons(crew)
    persons = [CrewPerson(*p) for p in persons]

    for p, person in enumerate(persons):
        await db.upsert_person(person)
        if p % 100 == 0:
            print(f'import crew persons in {p / len(persons) * 100:.1f}% done')

    await sleep(1)


if __name__ == "__main__":
    run(createCrew())
