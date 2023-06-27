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

    async def get_videos(self, offset=0, limit=500) -> list[Video]:
        async with self.pool.acquire() as connection:
            rows = await connection.fetch('select * from videos order by title offset $1 limit $2', offset, limit)
        return [Video(**dict(r)) for r in rows]

    async def is_like_set(self, video_id: UUID, user_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            ans = await connection.fetch('select count(*) = 0 from video_likes where video_id=$1 and user_id=$2',
                                         video_id, user_id)
        return not ans

    async def set_like(self, video_id: UUID, user_id: UUID, like_level: bool):
        # fixme: allows multiple likes of the same video_id by channel_id
        if await self.is_like_set(video_id, user_id):
            async with self.pool.acquire() as connection:
                await connection.fetch('update video_likes set is_liked=$1 where video_id=$2 and user_id=$3',
                                       like_level, video_id, user_id)
        else:
            async with self.pool.acquire() as connection:
                await connection.fetch('insert into video_likes(video_id, user_id, is_liked)'
                                       'values ($1, $2, $3) returning *', video_id, user_id, like_level)

    async def remove_like(self, video_id: UUID, channel_id: UUID):
        # delete from video_likes where video_id=$1 and channel_id=$2
        pass

    async def is_top_level_comment(self, parent_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            ans = await connection.fetch('select parent_comment is null from comments where comment_id = $1', parent_id)
        return ans

    async def is_spam(self, user_id: UUID, video_id: UUID) -> bool:
        async with self.pool.acquire() as connection:
            # note: fetch returns Recort<False> (not a bool); fetchval returns a bool
            ans = await connection.fetchval(
                """select exists (select 1 from comments where user_id = $1 and video_id = $2)""",
                user_id, video_id)

        return ans

    async def post_comment(self, user_id: UUID, content: str, video_id: UUID, parent_id: UUID | None) -> Comment:
        if parent_id is not None:
            if not (await self.is_top_level_comment(parent_id)):
                raise ReplayException('Comments nesting cannot be deeper than 1 level')

        # todo: consider using unique(video_id, channel_id) constraint on video_likes table
        if not await self.is_spam(user_id, video_id):
            async with self.pool.acquire() as connection:
                new_comment = await connection.fetch(
                    'insert into comments(user_id, content, video_id, parent_id) values'
                    '($1, $2, $3, $4) returning *', user_id, content, video_id, parent_id)
                return new_comment
        else:
            raise ReplayException('You spammer!')


async def main_():
    db = DbService()
    await db.initialize()
    videos = await db.get_videos()
    print(videos)
    video_id = UUID('84aba99c-6307-463c-afda-be6d1bc7d58d')
    user_id = UUID('e1411932-5825-458c-81cd-39a4a1313230')
    await db.set_like(video_id, user_id, like_level=True)
    await db.post_comment(user_id, 'test', video_id, parent_id=None)


if __name__ == '__main__':
    run(main_())
