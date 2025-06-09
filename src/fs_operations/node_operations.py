from src.utils.models import FileSystemNode, Permission, LocalState
from src.utils import split_path, normalize_path, get_parent_path, get_basename
from src.permissions.permissions_manager import PermissionManager
import fnmatch
from typing import List
import os

"""
All operations supported by the filesystem (applies to both files and directories)
"""
class NodeOperations:
    def __init__(self, local: LocalState, perm_manager: PermissionManager = None):
        self.local = local
        self.root = local.root
        self.perm_manager = perm_manager

    """Get the path of a node"""
    def _get_path(self, node):
        if not node:
            return "/"
        if node == self.root:
            return "/"
        path = []
        current = node
        while current and current != self.root:
            path.append(current.name)
            current = current.parent
        if not path:
            return "/"
        return "/" + "/".join(reversed(path))

    """Move a node (file or directory)"""
    def move(self, name, new_name):
        cwd = self.local.cwd
        with cwd.lock:
            # Check write permission on current directory
            self.perm_manager.check_permission(cwd, "write")
            
            # Check if source exists
            if name not in cwd.children:
                raise Exception(f"'{name}' not found")
            
            # Handle destination with trailing slash (directory move)
            if new_name.endswith('/'):
                # Remove trailing slash
                dest_dir_name = new_name.rstrip('/')
                
                # Check if destination directory exists
                if dest_dir_name not in cwd.children:
                    raise Exception(f"Destination directory '{dest_dir_name}' not found")
                
                dest_dir = cwd.children[dest_dir_name]
                if not dest_dir.is_directory:
                    raise Exception(f"'{dest_dir_name}' is not a directory")
                
                # Check write permission on destination directory
                self.perm_manager.check_permission(dest_dir, "write")
                
                # Move node to destination directory
                node = cwd.remove_child(name)
                dest_dir.add_child(node)
                return True, dest_dir_name  # Return success and destination info
            else:
                # Regular move/rename
                if new_name in cwd.children:
                    raise Exception(f"'{new_name}' already exists")
                node = cwd.remove_child(name)
                node.name = new_name
                cwd.add_child(node)
                return False, new_name  # Return success and destination info

    """Check if a node exists in current directory"""
    def _check_node_exists(self, name: str, should_exist: bool = True) -> FileSystemNode:
        exists = name in self.local.cwd.children
        if should_exist and not exists:
            raise ValueError(f"{name} not found")
        elif not should_exist and exists:
            raise ValueError(f"{name} already exists")
        return self.local.cwd.children.get(name)

    """Create a new node (file or directory)"""
    def _create_node(self, name: str, is_directory: bool = False) -> FileSystemNode:
        cwd = self.local.cwd
        with cwd.lock:
            self.perm_manager.check_permission(cwd, "write")
            self._check_node_exists(name, should_exist=False)
            
            # Create new node
            node = FileSystemNode(name, owner=self.local.user, is_directory=is_directory)
            node.permissions[self.local.user] = Permission(owner=self.local.user, read=True, write=True)
            
            # Set up parent-child relationship
            node.parent = cwd
            cwd.children[name] = node
            
            return node

    """Get node at specified path"""
    def get_node(self, path: str) -> FileSystemNode:
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
    def _find_recursive(self, node: FileSystemNode, pattern: str) -> List[str]:
        result = []
        if fnmatch.fnmatch(node.name, pattern):
            result.append(node.name)
            
        if node.is_directory:
            for child in node.children.values():
                try:
                    self.perm_manager.check_permission(child, "read")
                    child_matches = self._find_recursive(child, pattern)
                    result.extend([os.path.join(node.name, match) for match in child_matches])
                except:
                    continue
        return result 