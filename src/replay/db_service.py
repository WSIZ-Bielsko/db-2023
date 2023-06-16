from asyncio import run
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

    async def create_channel(self, username: str) -> UUID:
        async with self.pool.acquire() as connection:
            chan = await connection.fetchval('INSERT INTO channel(username) VALUES ($1) RETURNING *', username)
        return chan

    async def get_videos(self, offset=0, limit=500) -> list[Video]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetchval('SELECT * FROM video ORDER BY title OFFSET $1 LIMIT $2', offset, limit)
        return rows

    async def create_video(self, title: str, owner_id: UUID, filename: str, file_content: bytes,
                           description: str) -> UUID:
        async with self.pool.acquire() as connection:
            vid = await connection.fetchval('INSERT INTO video(title, owner_id, filename, file_content, description) '
                                            'VALUES ($1, $2, $3, $4, $5) RETURNING *', title, owner_id, filename,
                                            file_content, description)
        return vid

    async def is_like_set(self, video_id: UUID, channel_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            ans = await connection.fetchval('SELECT EXISTS (SELECT 1 FROM video_likes WHERE video_id=$1 AND '
                                         'channel_id=$2)', video_id, channel_id)
        return not ans

    async def set_like(self, video_id: UUID, channel_id: UUID, like_level: bool):
        if await self.is_like_set(video_id, channel_id):
            async with self.pool.acquire() as connection:
                await connection.fetchval('UPDATE video_likes SET is_like=$1 WHERE video_id=$2 AND channel_id=$3',
                                          like_level, video_id, channel_id)
        else:
            async with self.pool.acquire() as connection:
                await connection.fetchval('INSERT INTO video_likes(video_id, channel_id, is_like) '
                                          'VALUES ($1, $2, $3) RETURNING *', video_id, channel_id, like_level)

    async def remove_like(self, video_id: UUID, channel_id: UUID):
        async with self.pool.acquire() as connection:
            await connection.fetchval('DELETE FROM video_likes WHERE video_id=$1 AND channel_id=$2', video_id,
                                      channel_id)

    async def is_top_level_comment(self, parent_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            ans = await connection.fetchval('SELECT parent_comment IS NULL FROM comment WHERE comment_id = $1',
                                            parent_id)
        return ans

    async def post_comment(self, author: UUID, content: str, video_id: UUID, parent_comment: UUID | None) -> UUID:
        if parent_comment is not None:
            if not await self.is_top_level_comment(parent_comment):
                raise ReplayException('Comments nesting cannot be deeper than 1 level')
        async with self.pool.acquire() as connection:
            com = await connection.fetchval('INSERT INTO comment(author_id, content, video_id, parent_comment) VALUES'
                                            '($1, $2, $3, $4) RETURNING *', author, content, video_id, parent_comment)
        return com


async def main_():
    from pathlib import Path
    db = DbService()
    await db.initialize()
    john_id = await db.create_channel('jan')
    jane_id = await db.create_channel('joanna')
    file_content = Path('kulka.webm').read_bytes()
    video_id = await db.create_video('kulka', john_id, 'kulka.webm', file_content, 'blender jest super')
    videos = await db.get_videos()
    print(videos)
    await db.set_like(video_id, jane_id, False)
    await db.set_like(video_id, jane_id, True)
    await db.remove_like(video_id, jane_id)
    alice_comment_id = await db.post_comment(jane_id, 'fajny film', video_id, None)
    bob_reply_id = await db.post_comment(john_id, 'dzieki', video_id, alice_comment_id)
    await db.post_comment(jane_id, '<3', video_id, bob_reply_id)  # <- this line should throw ReplayException


if __name__ == '__main__':
    run(main_())
