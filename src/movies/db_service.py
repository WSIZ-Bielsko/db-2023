from __future__ import annotations

from asyncio import run, sleep
from uuid import uuid4

import asyncpg
from dotenv import load_dotenv
from os import getenv

from model import *

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')


class DbService:

    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5, min_size=15, max_size=20,
                                              server_settings={'search_path': SCHEMA})

        print('connected!')

    # actors

    async def get_actors(self, offset=0, limit=500) -> list[Actor]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from actors order by name offset $1 limit $2', offset, limit)
        return [Actor(**dict(r)) for r in rows]

    async def get_actor(self, actor_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from actors where actor_id=$1', actor_id)
        return Actor(**dict(row)) if row else None

    async def upsert_actor(self, actor: Actor) -> Actor:
        if actor.actor_id is None:
            # insert; `actor` as no id assigned
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into actors(name) VALUES ($1) returning *",
                                                actor.name)
        elif await self.get_actor(actor.actor_id) is None:
            # insert; `actor` has id assigned externally
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into actors(actor_id,name) VALUES ($1,$2) returning *",
                                                actor.actor_id, actor.name)
        else:
            # update; `actor` with given id exists in db
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update actors set name=$2 where actor_id=$1 returning *""",
                                                actor.actor_id, actor.name)

        return Actor(**dict(row))

    # movies

    async def get_movies(self, offset=0, limit=500) -> list[Movie]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from movies order by title offset $1 limit $2', offset, limit)
        return [Movie(**dict(r)) for r in rows]

    async def get_movie(self, movie_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movies where movie_id=$1', movie_id)
        return Movie(**dict(row)) if row else None

    async def upsert_movie(self, movie: Movie) -> Movie:
        if movie.movie_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into movies(title,budget,popularity,release_date,revenue) 
                        VALUES ($1,$1,$2,$3,$4,$5) returning *""",
                    movie.title, movie.budget, movie.popularity, movie.release_date, movie.revenue)
        elif await self.get_movie(movie.movie_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into movies(movie_id,title,budget,popularity,release_date,revenue) 
                    VALUES ($1,$2,$3,$4,$5,$6) returning *""",
                    movie.movie_id, movie.title, movie.budget, movie.popularity, movie.release_date, movie.revenue)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update movies set title=$2, budget = $3,
                                                popularity = $4,
                                                release_date = $5,
                                                revenue = $6 where movie_id=$1 returning *""",
                                                movie.movie_id, movie.title, movie.budget, movie.popularity,
                                                movie.release_date, movie.revenue)

        return Movie(**dict(row))

    async def get_movieactor(self, movie_id: int, actor_id: int) -> MovieActor | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_actors where movie_id=$1 and actor_id=$2',
                                            movie_id, actor_id)
        return MovieActor(**dict(row)) if row else None

    async def upsert_movieactor(self, movie_actor: MovieActor) -> MovieActor:
        ma = movie_actor
        if await self.get_movieactor(ma.movie_id, ma.actor_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into movie_actors(movie_id, actor_id, cast_id, "
                                                "character, credit_id, gender, order_) VALUES "
                                                "($1,$2,$3,$4,$5,$6,$7) returning *",
                                                ma.movie_id, ma.actor_id, ma.cast_id, ma.character,
                                                ma.credit_id, ma.gender, ma.order_)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update movie_actors set cast_id=$3, character=$4, credit_id=$5,
                        gender=$6, order_=$7 where movie_id=$1 and actor_id=$2 returning *""",
                                                ma.movie_id, ma.actor_id, ma.cast_id, ma.character,
                                                ma.credit_id, ma.gender, ma.order_
                                                )

        return MovieActor(**dict(row))

    # movie actor

    async def get_movie_actor(self, movie_id: int, actor_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_actors where movie_id=$1 and actor_id=$2', movie_id,
                                            actor_id)
        return MovieActor(**dict(row)) if row else None

    async def get_movie_actors(self, offset=0, limit=500) -> list[Actor]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from movie_actors order by name offset $1 limit $2', offset, limit)
        return [Actor(**dict(r)) for r in rows]

    async def upsert_movie_actor(self, movie_actor: MovieActor) -> MovieActor:
        if await self.get_movie_actor(movie_actor.movie_id, movie_actor.actor_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into movie_actors(cast_id,movie_id,actor_id,credit_id,character,gender,position) 
                        VALUES ($1,$2, $3, $4, $5, $6, $7) returning *""",
                    movie_actor.cast_id, movie_actor.movie_id, movie_actor.actor_id, movie_actor.credit_id,
                    movie_actor.character, movie_actor.gender, movie_actor.position)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """update movie_actors set 
                        movie_id=$2, actor_id=$3, credit_id=$4, character=$5, gender=$6, position=$7  
                        where cast_id=$1 returning *""",
                    movie_actor.cast_id, movie_actor.movie_id, movie_actor.actor_id, movie_actor.credit_id,
                    movie_actor.character, movie_actor.gender, movie_actor.position)

        return MovieActor(**dict(row))

    # genre

    async def get_genre(self, genre_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from genres where genre_id=$1', genre_id)
        return Genre(**dict(row)) if row else None

    async def get_genres(self, offset=0, limit=500) -> list[Genre]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from genres order by name offset $1 limit $2', offset, limit)
        return [Genre(**dict(r)) for r in rows]

    async def upsert_genre(self, genre: Genre) -> Genre:
        if genre.genre_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into genres(name) VALUES ($1) returning *",
                                                genre.name)
        elif await self.get_genre(genre.genre_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into genres(genre_id,name) VALUES ($1,$2) returning *",
                                                genre.genre_id, genre.name)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update genres set name=$2 where genre_id=$1 returning *""",
                                                genre.genre_id, genre.name)

        return Genre(**dict(row))

    # crew

    async def get_crew(self, credit_id: str) -> Crew:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from crew where credit_id=$1', credit_id)
        return Crew(**dict(row)) if row else None

    async def get_crews(self, offset=0, limit=500) -> list[Crew]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from crew order by name offset $1 limit $2', offset, limit)
        return [Crew(**dict(r)) for r in rows]

    @staticmethod
    async def __get_new_crew_id() -> str:
        w = uuid4()
        w = str(w).replace('-', '')[:25]
        return w

    async def upsert_crew(self, crew: Crew) -> Crew:
        if crew.credit_id is None:
            crew.credit_id = self.__get_new_crew_id()

        c = crew  # alias
        if await self.get_crew(crew.credit_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """insert into crew(credit_id, movie_id, department, gender, id, job, name) 
                        VALUES ($1,$2,$3,$4,$5,$6,$7) returning *""",
                    c.credit_id, c.movie_id, c.department, c.gender, c.id, c.job, c.name)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """update crew set movie_id=$2, departament=$3, gender=$4, id=$5, job=$6, name=$7 where
                        credit_id=$1""", c.credit_id, c.movie_id, c.department, c.gender, c.id, c.job, c.name)

        return Crew(**dict(row))

    # movie genre

    async def get_movie_genre(self, genre_id: int, movie_id: int):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_genres where genre_id=$1 and movie_id=$2', genre_id,
                                            movie_id)
        return MovieGenre(**dict(row)) if row else None

    async def get_movie_genres(self, offset=0, limit=500) -> list[Genre]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from movie_genres order by name offset $1 limit $2', offset, limit)
        return [MovieGenre(**dict(r)) for r in rows]

    async def upsert_movie_genre(self, genre_id, movie_id) -> MovieGenre:
        if genre_id is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("insert into movie_genres(genre_id) VALUES ($1) returning *",
                                                genre_id)
        elif await self.get_movie_genre(genre_id, movie_id) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    "insert into movie_genres(genre_id,movie_id) VALUES ($1,$2) returning *",
                    genre_id, movie_id)
        else:
            # update

            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""update movie_genres set genre_id=$2 where movie_id=$1 returning *""",
                                                movie_id, genre_id)

        return MovieGenre(**dict(row))

    # pcountry

    async def get_pcountry(self, iso: str):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('SELECT * FROM pcountries WHERE iso_3166_1=$1', iso)
        return PCountry(**dict(row)) if row else None

    async def get_pcountries(self, offset=0, limit=500) -> list[PCountry]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('SELECT * FROM pcountries ORDER BY name OFFSET $1 LIMIT $2', offset, limit)
        return [PCountry(**dict(r)) for r in rows]

    async def upsert_pcountry(self, pcountry: PCountry) -> PCountry:
        if pcountry.iso_3166_1 is None:
            raise ValueError("PCountry must have iso_3166_1 value.")

        async with self.pool.acquire() as connection:
            if pcountry.name is None:
                row = await connection.fetchrow(
                    "insert into pcountries(iso_3166_1) VALUES ($1) returning *",
                    pcountry.iso_3166_1,
                )
            else:
                row = await connection.fetchrow(
                    "insert into pcountries(iso_3166_1, name) VALUES ($1, $2) "
                    "on conflict (iso_3166_1) do update set name = $2 returning *",
                    pcountry.iso_3166_1,
                    pcountry.name,
                )

        return PCountry(**dict(row))

    # movie pcountry

    async def get_movie_pcountry(self, movie_id: int, iso_3166_1: str):
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('select * from movie_pcountries where movie_id=$1 and iso_3166_1=$2',
                                            movie_id, iso_3166_1)
        return MoviePCountry(**dict(row)) if row else None

    async def get_movie_pcountries(self, offset=0, limit=500) -> list[MoviePCountry]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch(
                'select * from movie_pcountries order by movie_id, iso_3166_1 offset $1 limit $2', offset, limit)
        return [MoviePCountry(**dict(r)) for r in rows]

    async def upsert_movie_pcountry(self, movie_pcountry: MoviePCountry) -> MoviePCountry:
        movie_id = movie_pcountry.movie_id
        iso_3166_1 = movie_pcountry.iso_3166_1
        if await self.get_movie_pcountry(movie_id, iso_3166_1) is None:
            # insert
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow("""insert into movie_pcountries(movie_id, iso_3166_1) 
                                                    VALUES ($1,$2) returning *""",
                                                movie_id, iso_3166_1)
        else:
            # update
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(
                    """update movie_pcountries set movie_id=$1 where iso_3166_1=$2 returning *""",
                    movie_id, iso_3166_1)

        return MoviePCountry(**dict(row))

    # reporting helper methods

    async def get_most_popular_movies(self, year: int, count=10) -> list[Movie]:
        """

        :param year:
        :return: Full movie objects containing not more than `count` instances of most popular movies
            (movie.popularity)
        """
