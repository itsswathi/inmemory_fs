import pytest
from src.utils.models import FileSystemNode, Permission
from src.fs_operations.node_operations import NodeOperations
from src.fs_operations.file_operations import FileOperations
from src.fs_operations.directory_operations import DirectoryOperations
from src.permissions.user_operations import UserOperations
from src.permissions.group_operations import GroupOperations, PermissionGroup
from src.permissions.permissions_manager import PermissionManager

class LocalState:
    def __init__(self):
        self.user = "admin"
        self.cwd = None

@pytest.fixture
def local_state():
    return LocalState()

@pytest.fixture
def root_node():
    root = FileSystemNode("/", is_directory=True)
    root.perms = Permission(owner="admin", group="admins")
    return root

@pytest.fixture
def users():
    return {"admin": "admin123"}

@pytest.fixture
def groups():
    admins = PermissionGroup("admins", read=True, write=True)
    admins.members.add("admin")
    return {"admins": admins}

@pytest.fixture
def node_ops(root_node, local_state):
    return NodeOperations(root_node, local_state)

@pytest.fixture
def file_ops(root_node, local_state):
    return FileOperations(root_node, local_state)

@pytest.fixture
def dir_ops(root_node, local_state):
    return DirectoryOperations(root_node, local_state)

@pytest.fixture
def user_ops(users, local_state):
    return UserOperations(users, local_state)

@pytest.fixture
def group_ops(groups, users, local_state):
    return GroupOperations(groups, users, local_state)

@pytest.fixture
def perms_manager(root_node, local_state):
    return PermissionManager(root_node, local_state) 