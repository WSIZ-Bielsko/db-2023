from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Account:
    account_id: UUID
    account_name: str
    balance: float


if __name__ == '__main__':
    u = Account(uuid4(), 'ff', 100)
    print(u)
