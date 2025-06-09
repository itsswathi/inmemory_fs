import pytest
from src.utils.models import FileSystemNode, Permission, LocalState
from src.fs_operations.node_operations import NodeOperations
from src.fs_operations.file_operations import FileOperations
from src.fs_operations.directory_operations import DirectoryOperations
from src.permissions.user_operations import UserOperations
from src.permissions.group_operations import GroupOperations, PermissionGroup
from src.permissions.permissions_manager import PermissionManager

@pytest.fixture
def root_node():
    root = FileSystemNode("/", owner="admin", is_directory=True)
    root.permissions["admin"] = Permission(owner="admin", read=True, write=True)
    return root

@pytest.fixture
def local_state(root_node):
    local = LocalState(user="admin", cwd=root_node)
    local.users = {"admin": "admin123"}
    local.groups = {"admins": PermissionGroup("admins", read=True, write=True)}
    local.groups["admins"].members.add("admin")
    return local

@pytest.fixture
def node_ops(local_state):
    return NodeOperations(local_state)

@pytest.fixture
def file_ops(local_state):
    return FileOperations(local_state)

@pytest.fixture
def dir_ops(local_state):
    return DirectoryOperations(local_state)

@pytest.fixture
def user_ops(local_state):
    return UserOperations(local_state.users, local_state)

@pytest.fixture
def group_ops(local_state):
    return GroupOperations(local_state.groups, local_state.users, local_state)

@pytest.fixture
def perms_manager(local_state):
    return PermissionManager(local_state.cwd, local_state) 