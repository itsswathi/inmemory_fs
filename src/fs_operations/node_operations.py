from src.utils.models import FileSystemNode, Permission, LocalState
from src.utils import split_path, normalize_path, get_parent_path, get_basename
from src.permissions.permissions_manager import PermissionManager

"""
All operations supported by the filesystem (applies to both files and directories)
"""
class NodeOperations:
    def __init__(self, root_node: FileSystemNode, local: LocalState, perm_manager: PermissionManager = None):
        self.root = root_node
        self.local = local
        self.perm_manager = perm_manager

    """Get the path of a node"""
    def _get_path(self, node):
        path = []
        while node and node != self.root:
            path.append(node.name)
            node = node.parent
        return "/" + "/".join(reversed(path))

    """Move a node (file or directory)"""
    def move(self, name, new_name):
        cwd = self.local.cwd
        with cwd.lock:
            self.perm_manager.check_permission(cwd, "write")
            if name not in cwd.children:
                raise Exception(f"'{name}' not found")
            if new_name in cwd.children:
                raise Exception(f"'{new_name}' already exists")
            node = cwd.children.pop(name)
            node.name = new_name
            cwd.children[new_name] = node

    """Check if a node exists in current directory"""
    def _check_node_exists(self, name, should_exist=True):
        cwd = self.local.cwd
        exists = name in cwd.children
        if should_exist and not exists:
            raise Exception(f"'{name}' not found")
        elif not should_exist and exists:
            raise Exception(f"'{name}' already exists")
        return cwd.children.get(name) if exists else None

    """Create a new node (file or directory)"""
    def _create_node(self, name, is_directory=False):
        cwd = self.local.cwd
        with cwd.lock:
            self.perm_manager.check_permission(cwd, "write")
            self._check_node_exists(name, should_exist=False)
            node = FileSystemNode(name, is_directory=is_directory, owner=self.local.user)
            node.parent = cwd
            node.permissions[self.local.user] = Permission()
            cwd.children[name] = node
            return node

    def get_node(self, path: str) -> FileSystemNode:
        """Get node at specified path"""
        path = normalize_path(path)
        if path == "/":
            return self.root
            
        parts = split_path(path)
        current = self.root
        
        for part in parts[1:]:
            if not current.is_directory:
                raise Exception("Cannot traverse through file")
            if part not in current.children:
                raise Exception(f"Node {part} not found")
            current = current.children[part]
            
        return current

    """Get parent path of a node"""
    def get_parent_path(self, path: str) -> str:
        return get_parent_path(path)

    """Get basename of a node"""
    def get_basename(self, path: str) -> str:
        return get_basename(path)

    """Find a node by name in the current directory"""
    def find(self, name: str) -> FileSystemNode:
        return self.local.cwd.children.get(name)

    """Find a node recursively"""
    def _find_recursive(self, node, name):
        result = []
        with node.lock:
            for child in node.children.values():
                try:
                    self.perm_manager.check_permission(child, "read")
                    if child.name == name:
                        result.append(self._get_path(child))
                    if child.is_directory:
                        result.extend(self._find_recursive(child, name))
                except PermissionError:
                    continue
        return result 