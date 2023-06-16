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
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5, server_settings={'search_path': SCHEMA})

    async def create_channel(self, username: str) -> UUID:
        async with self.pool.acquire() as connection:
            chan = await connection.fetchval('INSERT INTO channel(username) VALUES ($1) RETURNING *', username)
        return chan

    async def get_videos(self, offset=0, limit=500) -> list[Video]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetchval('SELECT * FROM video ORDER BY title OFFSET $1 LIMIT $2', offset, limit)
        return rows

    async def create_video(self, title: str, owner_id: UUID, filename: str, description: str) -> UUID:
        async with self.pool.acquire() as connection:
            vid = await connection.fetchval('INSERT INTO video(title, owner_id, filename, description) VALUES'
                                            '($1, $2, $3, $4) RETURNING *', title, owner_id, filename, description)
        return vid

    async def is_like_set(self, video_id: UUID, channel_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            ans = await connection.fetch('SELECT count(*) = 0 FROM video_likes WHERE video_id=$1 AND channel_id=$2',
                                         video_id, channel_id)
        return not ans

    async def set_like(self, video_id: UUID, channel_id: UUID, like_level: bool):
        if await self.is_like_set(video_id, channel_id):
            async with self.pool.acquire() as connection:
                await connection.fetch('UPDATE video_likes SET is_like=$1 WHERE video_id=$2 AND channel_id=$3',
                                       like_level, video_id, channel_id)
        else:
            async with self.pool.acquire() as connection:
                await connection.fetch('INSERT INTO video_likes(video_id, channel_id, is_like)'
                                       'VALUES ($1, $2, $3) RETURNING *', video_id, channel_id, like_level)

    async def remove_like(self, video_id: UUID, channel_id: UUID):
        async with self.pool.acquire() as connection:
            await connection.fetch('DELETE FROM video_likes WHERE video_id=$1 AND channel_id=$2', video_id, channel_id)

    async def is_top_level_comment(self, parent_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            ans = await connection.fetchval('SELECT parent_comment IS NULL FROM comment WHERE comment_id = $1', parent_id)
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
    db = DbService()
    await db.initialize()
    alice_id = await db.create_channel('alice')
    bob_id = await db.create_channel('bob')
    video_id = await db.create_video('good video', bob_id, 'good video.MOV', 'good video')
    videos = await db.get_videos()
    print(videos)
    await db.set_like(video_id, alice_id, True)
    await db.set_like(video_id, alice_id, False)
    await db.remove_like(video_id, alice_id)
    alice_comment_id = await db.post_comment(alice_id, 'nice video', video_id, None)
    bob_reply_id = await db.post_comment(bob_id, 'thanks', video_id, alice_comment_id)
    await db.post_comment(alice_id, 'THIS SHOULD THROW EXCEPTION', video_id, bob_reply_id)

if __name__ == '__main__':
    run(main_())
