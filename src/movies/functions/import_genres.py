from db_services import DbService
from functions import *
from asyncio import *


async def createGenres():
    db = DbService()
    await db.initialize()

    f = '../data/tmdb_5000_movies.csv'
    genres = get_genres(f)

    for i, genre in enumerate(genres):
        await db.upsert_genre(genre)
        if i % 100 == 0:
            print(f'import in {i / len(genres) * 100:.1f}% done')

    await sleep(1)


if __name__ == "__main__":
    run(createGenres())
