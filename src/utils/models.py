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

    def __getstate__(self):
        state = self.__dict__.copy()
        # Don't pickle the lock
        del state['lock']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Recreate the lock
        self.lock = threading.RLock()

    def add_child(self, child: 'FileSystemNode'):
        """Add a child node and set its parent"""
        self.children[child.name] = child
        child.parent = self

    def remove_child(self, name: str) -> Optional['FileSystemNode']:
        """Remove a child node and clear its parent"""
        if name in self.children:
            child = self.children.pop(name)
            child.parent = None
            return child
        return None

@dataclass
class LocalState:
    def __init__(self, user: str = "admin", cwd: 'FileSystemNode' = None):
        self.user = user
        self.users = {"admin": "admin123"}  # username -> password
        self.groups = {}  # groupname -> PermissionGroup
        
        # Initialize root node if not provided
        if not cwd:
            root = FileSystemNode("/", owner="admin", is_directory=True)
            root.permissions["admin"] = Permission(owner="admin", read=True, write=True)
            self.root = root
            self.cwd = root
        else:
            # Find the root node by traversing up from cwd
            current = cwd
            while current.parent:
                current = current.parent
            self.root = current
            self.cwd = cwd

    def __getstate__(self):
        return {
            'user': self.user,
            'cwd': self.cwd,
            'root': self.root,
            'users': self.users,
            'groups': self.groups
        }

    def __setstate__(self, state):
        self.user = state['user']
        self.users = state['users']
        self.groups = state['groups']
        
        # Initialize root node if not present
        if 'root' not in state or not state['root']:
            self.root = FileSystemNode("/", owner="admin", is_directory=True)
            self.root.permissions["admin"] = Permission(owner="admin", read=True, write=True)
            self.cwd = self.root
        else:
            self.root = state['root']
            # If cwd is not in state or is None, set it to root
            if 'cwd' not in state or not state['cwd']:
                self.cwd = self.root
            else:
                self.cwd = state['cwd']
                # Ensure cwd has a valid path to root
                current = self.cwd
                while current and current != self.root:
                    if not current.parent:
                        # If we can't find a path to root, reset to root
                        self.cwd = self.root
                        break
                    current = current.parent