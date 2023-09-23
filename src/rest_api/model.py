from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime


class Lecture(BaseModel):
    lecture_id: UUID
    lecture_name: str


class Lecturer(BaseModel):
    lecturer_id: UUID
    lecturer_name: str


class Semester(BaseModel):
    semester_id: UUID
    semester_name: str
    semester_start: date = datetime.today()
    semester_end: date = datetime.today()


class Syllabus(BaseModel):
    syllabus_id: UUID
    lecture_id: UUID
    semester_id: UUID
    lecturer_id: UUID


class LectureContent(BaseModel):
    content_id: UUID
    order_number: int = 0
    syllabus_id: UUID
    lecture_topic: str
