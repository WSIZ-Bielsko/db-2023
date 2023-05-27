from dataclasses import dataclass
from datetime import datetime


@dataclass
class File:
    fileid: int        # PK
    name: str           # !null
    bytes: int          # >= 0
    depth: int          # >= 0
    accessed: datetime
    modified: datetime
    basename: str
    extension: str
    type: str   # tylko 'd' albo 'f'
    mode: str   # !null
    parentpath: str    # fullpath = parentpath || name || '%'
    fullpath: str # !null
