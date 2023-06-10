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

    async def get_videos(self, offset=0, limit=500) -> list[Video]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from video order by title offset $1 limit $2', offset, limit)
        return [Video(**dict(r)) for r in rows]

    async def is_like_set(self, video_id: UUID, channel_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            ans = await connection.fetch('select count(*) = 0 from video_likes where video_id=$1 and channel_id=$2',
                                         video_id, channel_id)
        return ans

    async def set_like(self, video_id: UUID, channel_id: UUID, like_level: bool):
        if await self.is_like_set(video_id, channel_id):
            async with self.pool.acquire() as connection:
                await connection.fetch('update video_likes set is_like=$1 where video_id=$2 and channel_id=$3',
                                       like_level, video_id, channel_id)
        else:
            async with self.pool.acquire() as connection:
                await connection.fetch('insert into video_likes(video_id, channel_id, is_like)'
                                       'values ($1, $2, $3) returning *', video_id, channel_id, like_level)

    async def is_parent_empty(self, parent_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            ans = await connection.fetch('select parent_comment is null from comment where comment_id = $1', parent_id)
        return ans

    async def is_spam(self, author: UUID, content: str, video_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            ans = await connection.fetch('select count(*) = 0 from comment where author = $1 and content = $2 '
                                         'and video_id = $3', author, content, video_id)
        return ans

    async def post_comment(self, author: UUID, content: str, video_id: UUID, parent_comment: UUID | None):
        if parent_comment is not None:
            if not await self.is_parent_empty(parent_comment):
                raise Exception('Comments nesting cannot be deeper than 1 level')
        if not await self.is_spam(author, content, video_id):
            async with self.pool.acquire() as connection:
                await connection.fetch('insert into comment(author, content, video_id, parent_comment) values'
                                       '($1, $2, $3, $4) returning *', author, content, video_id, parent_comment)


async def main_():
    db = DbService()
    await db.initialize()
    videos = await db.get_videos()
    print(videos)
    video, user = UUID('771c8d3e-1c32-4a9b-9cb1-6c278b52580c'), UUID('8aa66945-77b2-4bb2-bd17-00da523c561e')
    await db.set_like(video, user, True)
    await db.post_comment(user, 'test', video, None)

if __name__ == '__main__':
    run(main_())
