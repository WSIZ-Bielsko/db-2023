from asyncpg import create_pool
from dotenv import load_dotenv
from os import getenv
from model import *
from asyncio import run

load_dotenv()
URL = getenv('DATABASE_URL')
SCHEMA = getenv('SCHEMA')
ADDING_MESSAGE = 'Added {}'
REMOVING_MESSAGE = 'Removed {}'


class DbService:
    async def initialize(self):
        self.pool = await create_pool(URL, timeout=30, command_timeout=5, server_settings={'search_path': SCHEMA})

    async def get_lectures(self, offset=0, limit=500) -> list[Lecture] | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetch('SELECT * FROM lecture OFFSET $1 LIMIT $2', offset, limit)
            return [Lecture(**dict(r)) for r in row]

    async def get_lecture(self, lecture_id: UUID) -> Lecture | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('SELECT * FROM lecture WHERE lecture_id=$1', lecture_id)
            return Lecture(**dict(row)) if row else None

    async def upsert_lecture(self, lecture: Lecture) -> Lecture | None:
        async with self.pool.acquire() as connection:
            if lecture.lecture_id is None:
                row = await connection.fetchrow("""INSERT INTO lecture(lecture_name) VALUES ($1) RETURNING *""", lecture.lecture_name)
            elif await self.get_lecture(lecture.lecture_id) is None:
                row = await connection.fetchrow("""INSERT INTO lecture(lecture_id, lecture_name) VALUES($1, $2) RETURNING *""", lecture.lecture_id, lecture.lecture_name)
            else:
                row = await connection.fetchrow("""UPDATE lecture SET lecture_name=$2 WHERE lecture_id=$1 RETURNING *""", lecture.lecture_id, lecture.lecture_name)
            await log(ADDING_MESSAGE.format(row))
            return Lecture(**dict(row)) if row else None

    async def delete_lecture(self, lecture_id: UUID) -> Lecture | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('DELETE FROM lecture WHERE lecture_id=$1 RETURNING *', lecture_id)
            await log(REMOVING_MESSAGE.format(lecture_id))
            return Lecture(**dict(row))

    async def get_lecturers(self, offset=0, limit=500) -> list[Lecturer] | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetch('SELECT * FROM lecturer OFFSET $1 LIMIT $2', offset, limit)
            return [Lecturer(**dict(r)) for r in row]

    async def get_lecturer(self, lecturer_id: UUID) -> Lecturer | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('SELECT * FROM lecturer WHERE lecturer_id=$1', lecturer_id)
            return Lecturer(**dict(row)) if row else None

    async def upsert_lecturer(self, lecturer: Lecturer) -> Lecturer | None:
        async with self.pool.acquire() as connection:
            if lecturer.lecturer_id is None:
                row = await connection.fetchrow("""INSERT INTO lecturer(lecturer_name) VALUES ($1) RETURNING *""", lecturer.lecturer_name)
            elif await self.get_lecturer(lecturer.lecturer_id) is None:
                row = await connection.fetchrow("""INSERT INTO lecturer(lecturer_id, lecturer_name) VALUES($1, $2) RETURNING *""", lecturer.lecturer_id, lecturer.lecturer_name)
            else:
                row = await connection.fetchrow("""UPDATE lecturer SET lecturer_name=$2 WHERE lecturer_id=$1 RETURNING *""", lecturer.lecturer_id, lecturer.lecturer_name)
            await log(ADDING_MESSAGE.format(row))
            return Lecturer(**dict(row))

    async def delete_lecturer(self, lecturer_id: UUID) -> Lecturer | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('DELETE FROM lecturer WHERE lecturer_id=$1 RETURNING *', lecturer_id)
            await log(REMOVING_MESSAGE.format(lecturer_id))
            return Lecturer(**dict(row))

    async def get_semesters(self, offset=0, limit=500) -> list[Semester] | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetch('SELECT * FROM semester OFFSET $1 LIMIT $2', offset, limit)
            return [Semester(**dict(r)) for r in row]

    async def get_semester(self, semester_id: UUID) -> Semester | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('SELECT * FROM semester WHERE semester_id=$1', semester_id)
            return Semester(**dict(row)) if row else None

    async def upsert_semester(self, semester: Semester) -> Semester | None:
        async with self.pool.acquire() as connection:
            if semester.semester_id is None:
                row = await connection.fetchrow("""INSERT INTO semester(semester_name, semester_start, semester_end) VALUES ($1, $2, $3) RETURNING *""", semester.semester_name, semester.semester_start, semester.semester_end)
            elif await self.get_semester(semester.semester_id) is None:
                row = await connection.fetchrow("""INSERT INTO semester(semester_id, semester_name, semester_start, semester_end) VALUES($1, $2, $3, $4) RETURNING *""", semester.semester_id, semester.semester_name, semester.semester_start, semester.semester_end)
            else:
                row = await connection.fetchrow("""UPDATE semester SET semester_name=$2, semester_start=$3, semester_end=$4 WHERE semester_id=$1 RETURNING *""", semester.semester_id, semester.semester_name, semester.semester_start, semester.semester_end)
            await log(ADDING_MESSAGE.format(row))
            return Semester(**dict(row)) if row else None

    async def delete_semester(self, semester_id: UUID) -> Semester | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('DELETE FROM semester WHERE semester_id=$1 RETURNING *', semester_id)
            await log(REMOVING_MESSAGE.format(semester_id))
            return Semester(**dict(row)) if row else None

    async def get_syllabuses(self, offset=0, limit=500) -> list[Syllabus] | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetch('SELECT * FROM syllabus OFFSET $1 LIMIT $2', offset, limit)
            return [Syllabus(**dict(r)) for r in row]

    async def get_syllabus(self, syllabus_id: UUID) -> Syllabus | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('SELECT * FROM syllabus WHERE syllabus_id=$1', syllabus_id)
            return Syllabus(**dict(row)) if row else None

    async def upsert_syllabus(self, syllabus: Syllabus) -> Syllabus | None:
        async with self.pool.acquire() as connection:
            if syllabus.syllabus_id is None:
                row = await connection.fetchrow("""INSERT INTO syllabus(lecture_id, semester_id, lecturer_id) VALUES ($1, $2, $3) RETURNING *""", syllabus.lecture_id, syllabus.semester_id, syllabus.lecturer_id)
            elif await self.get_syllabus(syllabus.syllabus_id) is None:
                row = await connection.fetchrow("""INSERT INTO syllabus(syllabus_id, lecture_id, semester_id, lecturer_id) VALUES ($1, $2, $3, $4) RETURNING *""", syllabus.syllabus_id, syllabus.lecture_id, syllabus.semester_id, syllabus.lecturer_id)
            else:
                row = await connection.fetchrow("""UPDATE syllabus SET lecture_id=$2, semester_id=$3, lecturer_id=$4 WHERE syllabus_id=$1 RETURNING *""", syllabus.syllabus_id, syllabus.lecture_id, syllabus.semester_id, syllabus.lecturer_id)
            await log(ADDING_MESSAGE.format(row))
            return Syllabus(**dict(row)) if row else None

    async def delete_syllabus(self, syllabus_id: UUID) -> Syllabus | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('DELETE FROM syllabus WHERE syllabus_id=$1 RETURNING *', syllabus_id)
            await log(REMOVING_MESSAGE.format(syllabus_id))
            return Syllabus(**dict(row)) if row else None

    async def get_lectures_content(self, offset=0, limit=500) -> list[LectureContent] | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetch('SELECT * FROM lecture_content OFFSET $1 LIMIT $2', offset, limit)
            return [LectureContent(**dict(r)) for r in row]

    async def get_lecture_content(self, content_id: str) -> LectureContent | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('SELECT * FROM lecture_content WHERE content_id=$1', content_id)
            return LectureContent(**dict(row)) if row else None

    async def upsert_lecture_content(self, content: LectureContent) -> LectureContent | None:
        async with self.pool.acquire() as connection:
            if content.content_id is None:
                row = await connection.fetchrow("""INSERT INTO lecture_content(order_number, syllabus_id, lecture_topic) VALUES ($1, $2, $3) RETURNING *""", content.order_number, content.syllabus_id, content.lecture_topic)
            elif await self.get_syllabus(content.content_id) is None:
                row = await connection.fetchrow("""INSERT INTO lecture_content(content_id, order_number, syllabus_id, lecture_topic) VALUES ($1, $2, $3, $4) RETURNING *""", content.syllabus_id, content.order_number, content.syllabus_id, content.lecture_topic)
            else:
                row = await connection.fetchrow("""UPDATE lecture_content SET order_number=$2, syllabus_id=$3, lecture_topic=$4 WHERE content_id=$1 RETURNING *""", content.syllabus_id, content.order_number, content.syllabus_id, content.lecture_topic)
            await log(ADDING_MESSAGE.format(row))
            return LectureContent(**dict(row)) if row else None

    async def delete_lecture_content(self, content_id: UUID) -> LectureContent | None:
        async with self.pool.acquire() as connection:
            row = await connection.fetchrow('DELETE FROM lecture_content WHERE content_id=$1 RETURNING *', content_id)
            await log(REMOVING_MESSAGE.format(content_id))
            return LectureContent(**dict(row)) if row else None


async def log(message: str):
    print(f'[{datetime.now()}]: {message}')


async def main():
    db = DbService()
    await db.initialize()
    lectures = await db.get_lectures()
    print(dict(lectures))

if __name__ == '__main__':
    run(main())
