from asyncio import run, sleep
from ..functions import get_crew, get_crew_people, get_movie_crew
from ..db_service import DbService
from ..model import CrewPerson

#ONLY PEOPLE --------------
async def create_crew():
    db = DbService()
    await db.initialize()

    crew_ = get_crew()
    people = get_crew_people(crew_)
    people = [CrewPerson(*p) for p in people]

    for p, person in enumerate(people):
        await db.upsert_person(person)
        if p%100 == 0:
            print(f'import crew people in {p/len(people) *100:.1f}% done')

    await sleep(1)

#MOVIE PEOPLE ---------------
async def create_movie_crew():
    db = DbService()
    await db.initialize()

    filename = './datas/tmdb_5000_credits.csv'
    movie_crew = get_movie_crew(filename)

    for mc, mcrew in enumerate(movie_crew):
        await db.upsert_movie_crew(mcrew)
        if mc% 100== 0:
            print(f'import movie crew in {mc/len(movie_crew)*100:.1f}% done')

    await sleep(1)


if __name__ == "__main__":
    run(create_movie_crew())