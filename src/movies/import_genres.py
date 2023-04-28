from asyncio import run, sleep

import asyncpg
from dotenv import load_dotenv
from os import getenv

import pandas as pd

import json

from db_class import DbService

from model import Actor
from src.movies.analysis_tools import *


async def main():
    db = DbService()
    await db.initialize()  # tu łączymy się z bazą danych

    genres = get_genres()
    print(len(genres))

    for i, genre in enumerate(genres):
        await db.upsert_genre(genre)
        if i % 100 == 0:
            print(f'import in {i / len(genres) * 100:.1f}% done')

    await sleep(1)


if __name__ == '__main__':
    run(main())
