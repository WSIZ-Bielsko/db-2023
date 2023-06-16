from dataclasses import dataclass
from datetime import datetime


@dataclass
class File:
    file_id: int
    name: str
    bytes: int
    depth: int
    accessed: datetime
    modified: datetime
    basename: str
    extension: str
    type: str
    mode: str
    parent_path: str
    full_path: str
