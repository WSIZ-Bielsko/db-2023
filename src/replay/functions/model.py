from dataclasses import dataclass
from uuid import UUID


@dataclass
class Video:
    video_id: UUID
    title: str


@dataclass
class User:
    user_id: UUID
    username: str


@dataclass
class VideoLike:
    video_id: UUID
    user_id: UUID
    is_liked: bool


@dataclass
class Comment:
    comment_id: UUID
    video_id: UUID
    user_id: UUID
    parent_id: UUID
    content: str


class ReplayException(RuntimeError):
    pass
