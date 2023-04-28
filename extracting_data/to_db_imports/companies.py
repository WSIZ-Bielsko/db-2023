from asyncio import run, sleep
from ..functions import get_companies, get_company_of_movie
from ..db_service import DbService


# ONLY COMPANIES ----------------

async def create_companies():
    db = DbService()
    await db.initialize()

    companies = get_companies()

    for c, comp in enumerate(companies):
        await db.upsert_prod_company(comp)
        if c% 100== 0:
            print(f'import companies in {c/len(companies) *100:.1f}% done')

    await sleep(1)

# MOVIE COMPANIES -------------------
async def create_movie_companies():
    db = DbService()
    await db.initialize()

    movie_comps = get_company_of_movie()

    for mc, mcomp in enumerate(movie_comps):
        await db.upsert_movie_company(mcomp)
        if mc%100==0:
            print(f'insert movie companies in {mc/len(movie_comps)*100:.1f}% done')

    await sleep(1)

if __name__ == "__main__":
    run(create_movie_companies())