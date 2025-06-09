import threading
from datetime import datetime
from typing import Dict, Optional, Set
from dataclasses import dataclass, field

@dataclass
class Permission:
    owner: str = None
    group: str = None
    read: bool = True
    write: bool = False

class FileType:
    REGULAR = "regular"
    DIRECTORY = "directory"
    SYMLINK = "symlink"
    EXECUTABLE = "executable"

@dataclass
class FileSystemNode:
    name: str
    is_directory: bool = False
    owner: Optional[str] = None
    file_type: str = field(init=False)
    parent: Optional['FileSystemNode'] = None
    children: Dict[str, 'FileSystemNode'] = field(default_factory=dict)
    content: str = ""
    size: int = 0
    lock: threading.RLock = field(default_factory=threading.RLock)
    group: Optional[str] = None
    permissions: Dict[str, Permission] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    accessed_at: datetime = field(default_factory=datetime.now)
    target_path: Optional[str] = None
    tags: Set[str] = field(default_factory=set)
    mime_type: Optional[str] = None
    perms: Permission = field(default_factory=Permission)

    def __post_init__(self):
        self.file_type = FileType.DIRECTORY if self.is_directory else FileType.REGULAR
        if not self.is_directory:
            self.content = "" if self.content is None else self.content