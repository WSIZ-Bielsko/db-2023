from asyncio import run, sleep
import asyncpg
from dotenv import load_dotenv
from os import getenv
from model import *


load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')

class DbService:

    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5,
                                              server_settings={'search_path': SCHEMA})

        print('connected!')


    # MOVIES --------------------------------------
    async def get_movies(self, offset=0, limit=500) -> list[Movie]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from movies order by title offset $1 limit $2', offset, limit)
        return [Movie(**dict(r)) for r in rows]

    async def get_movie(self, movie_id: int) -> Movie | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movies where movie_id=$1', movie_id)
        return Movie(**dict(row)) if row else None

    async def upsert_movie(self, movie: Movie) -> Movie:
        if movie.movie_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into movies(title) VALUES ($1) returning *",
                                                movie.title)
        elif await self.get_movie(movie.movie_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into movies(movie_id,title) VALUES ($1,$2) returning *",
                                                movie.movie_id, movie.title)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update movies set title=$2 where movie_index=$1 returning *""",
                                                movie.movie_id, movie.title)

        return Movie(**dict(row))


    # ACTORS --------------------------------------
    async def get_actor(self, actor_id: int) -> Actor | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from actors where actor_id=$1', actor_id)
        return Actor(**dict(row)) if row else None

    async def get_actors(self, offset=0, limit=500) -> list[Actor]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from actors order by name offset $1 limit $2', offset, limit)
        return [Actor(**dict(r)) for r in rows]

    async def upsert_actor(self, actor: Actor) -> Actor:
        if actor.actor_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into actors(name) VALUES ($1) returning *",
                                                actor.name)
        elif await self.get_actor(actor.actor_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into actors(actor_id,name) VALUES ($1,$2) returning *",
                                                actor.actor_id, actor.name)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update actors set name=$2 where actor_id=$1 returning *""",
                                                actor.actor_id, actor.name)

        return Actor(**dict(row))


    # MOVIE_ACTORS --------------------------------------
    async def get_movie_actor(self, movie_id: int, actor_id: int) -> MovieActor | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_actors where movie_id=$1 and actor_id=$2',
                                            movie_id, actor_id)
        return MovieActor(**dict(row)) if row else None

    async def upsert_movie_actor(self, movie_actor: MovieActor) -> MovieActor:
        ma = movie_actor
        if await self.get_movie_actor(ma.movie_id, ma.actor_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into movie_actors(movie_id, actor_id, cast_id, "
                                                "character, credit_id, gender, orders) VALUES "
                                                "($1,$2,$3,$4,$5,$6,$7) returning *",
                                                ma.movie_id, ma.actor_id, ma.cast_id, ma.character,
                                                ma.credit_id, ma.gender, ma.orders)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update movie_actors set cast_id=$3, character=$4, credit_id=$5,
                        gender=$6, orders=$7 where movie_id=$1 and actor_id=$2 returning *""",
                                                ma.movie_id, ma.actor_id, ma.cast_id, ma.character,
                                                ma.credit_id, ma.gender, ma.orders
                                                )

        return MovieActor(**dict(row))


    #CREW --------------------------------------
    async def get_person(self, person_id: int) -> CrewPerson | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from crew where person_id=$1', person_id)
        return CrewPerson(**dict(row)) if row else None

    async def get_people(self, offset=0, limit=500) ->list[CrewPerson]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from crew order by person_id offset $1 limit $2',
                                          offset, limit)
        return [CrewPerson(**dict(r)) for r in rows]

    async def upsert_person(self, person: CrewPerson) -> CrewPerson:
        p = person
        if await self.get_person(p.person_id) is None:
            #insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('insert into crew(person_id, name) values ($1, $2)'
                                                'returning *', p.person_id, p.name)
        else:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update crew set name=$2 where person_id=$1 returning *""",
                                                p.person_id, p.name)

        return CrewPerson(**dict(row))


    #MOVIE_CREW --------------------------------------
    async def get_movie_crew(self, movie_id: int, person_id: int) -> MovieCrew | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_crew where movie_id=$1 and person_id=$2',
                                            movie_id, person_id)

        return MovieCrew(**dict(row)) if row else None

    async def upsert_movie_crew(self, movie_crew: MovieCrew) -> MovieCrew:
        mc = movie_crew
        if await self.get_movie_actor(mc.movie_id, mc.person_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into movie_crew(movie_index, person_id, credit_id, "
                                                "department, job, gender) VALUES "
                                                "($1,$2,$3,$4,$5,$6) returning *",
                                                mc.movie_id, mc.person_id, mc.credit_id, mc.department,
                                                mc.job, mc.gender)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update movie_crew set credit_id=$3, department=$4, job=$5,
                        gender=$6 where movie_index=$1 and person_id=$2 returning *""",
                                                mc.movie_id, mc.person_id, mc.credit_id, mc.department,
                                                mc.job, mc.gender
                                                )

        # return MovieCrew(**dict(row))
        return MovieCrew(movie_id=mc.movie_id, person_id=mc.person_id, credit_id=mc.credit_id,
                         department=mc.department, job=mc.job, gender=mc.gender)


    #LANGUAGES --------------------------------------
    async def get_language(self, lang_id: int) -> Language | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from languages '
                                            'where lang_id=$1', lang_id)
        result = Language(**dict(row)) if row else None


    async def get_languages(self, offset=0, limit=100) -> list[Language]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from languages '
                                          'order by lang_id offset $1 limit $2',
                                          offset, limit)
        return [Language(**dict(row)) for row in rows]

    async def upsert_language(self, language: Language) -> Language:
        l = language
        if await self.get_language(l.lang_id) is None:
            #insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('insert into languages(lang_id, lang) values ($1, $2)'
                                                'returning *', l.lang_id, l.lang)
        else:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('update languages set lang=$2 where lang_id=$1 returning *',
                                                l.lang_id, l.lang)
        return Language(**dict(row))


    #MOVIE LANGUAGES --------------------------------------
    async def get_movie_language(self, movie_id: int) -> MovieLanguage:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_languages '
                                            'where movie_id=$1', movie_id)
        result = MovieLanguage(**dict(row)) if row else None
        print(result)

    async def upsert_movie_language(self, movie_lang: MovieLanguage) -> MovieLanguage:
        ml = movie_lang
        if await self.get_movie_language(ml.movie_id) is None:
            #insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('insert into movie_languages(movie_id, lang_id) values ($1, $2)'
                                                'returning *', ml.movie_id, ml.lang_id)
        else:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('update movie_languages set lang_id=$2 where movie_id=$1 '
                                                'returning *', ml.movie_id, ml.lang_id)
        return MovieLanguage(**dict(row))

    #COMPANIES --------------------------------------
    async def get_prod_company(self, comp_id: int) -> Company | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from prod_companies where company_id=$1',
                                            comp_id)

            return Pcompany(**(row)) if row else None

    async def get_prod_companies(self, offset=0, limit=100) -> list[Company]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetchrow('select * from prod_companies '
                                             'order by company_id offset $1 limit $2',
                                             offset, limit)

        return [Pcompany(**dict(row)) for row in rows]

    async def upsert_prod_company(self, company: Company) -> Company:
        c = company
        if await self.get_prod_company(c.id) is None:
            #insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('insert into prod_companies(company_id, name) values ($1, $2)'
                                                'returning *', c.id, c.name)
        else:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('update prod_companies set name=$2 where company_id=$1 returning *',
                                                c.id, c.name)
        return Pcompany(**dict(row))

    #MOVIE COMPANIES --------------------------------------
    async def get_movie_company(self, movie_id: int) -> MovieCompany:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_prod_companies where movie_id=$1',
                                            movie_id)

        return MovieCompany(**dict(row)) if row else None

    async def upsert_movie_company(self, movie_comp: MovieCompany) -> MovieCompany:
        mc = movie_comp
        if await self.get_movie_company(mc.movie_id) is None:
            #insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('insert into movie_prod_companies(movie_id, company_id) values ($1, $2)'
                                                'returning *', mc.movie_id, mc.company_id)
        else:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow('update movie_prod_companies set company_id=$2 where movie_id=$1 '
                                                'returning *', mc.movie_id, mc.company_id)

        return MovieCompany(**dict(row))


    #GENRES --------------------------------------
    #MOVIE GENRES --------------------------------------


async def main_():
    db = DbService()
    await db.initialize()
    # await db.get_language(lang_id='en')
    await db.get_movie_language(movie_id=285)


if __name__ == '__main__':
    run(main_())
