from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class User:
    uid: UUID
    username: str
    password: str
    created_at: datetime
    updated_at: datetime


if __name__ == '__main__':
    u = User(uuid4(), 'Koala', '123', datetime.now(), datetime.now())
    print(u)
