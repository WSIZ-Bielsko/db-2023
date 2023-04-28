from asyncio import run, sleep

import asyncpg
from dotenv import load_dotenv
from os import getenv

import pandas as pd

import json

from db_class import DbService

from model import Movie
from src.movies.analysis_tools import get_movies


async def main():
    db = DbService()
    await db.initialize()  # tu łączymy się z bazą danych
    movies = get_movies('data/tmdb_5000_movies.csv')
    print(f'all movies: {len(movies)}')

    for i, movie in enumerate(movies):
        await db.upsert_movie(movie)
        if i % 100 == 0:
            print(f'import in {i / len(movies) * 100:.1f}% done')

    await sleep(1)


if __name__ == '__main__':
    run(main())
