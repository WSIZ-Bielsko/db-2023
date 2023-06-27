from dataclasses import dataclass
from datetime import datetime


@dataclass
class File:
    file_id: int  # PK
    name: str  # !null
    bytes: int  # >= 0
    depth: int  # >= 0
    accessed: datetime
    modified: datetime
    basename: str
    extension: str
    type: str  # tylko 'd' albo 'f'
    mode: str  # !null
    parent_path: str  # fullpath = parentpath || name || '%'
    full_path: str  # !null (ma być unikalny)
