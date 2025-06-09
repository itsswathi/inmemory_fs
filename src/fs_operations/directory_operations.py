from src.fs_operations.node_operations import NodeOperations
from src.utils.models import FileSystemNode, LocalState
from src.permissions.permissions_manager import PermissionManager
from typing import List

"""
All directory operations supported by the filesystem
"""
class DirectoryOperations(NodeOperations):
    def __init__(self, local: LocalState, perm_manager: PermissionManager = None):
        super().__init__(local, perm_manager)

    """Get the current working directory"""
    def pwd(self):
        return super()._get_path(self.local.cwd)

    """List the contents of the current directory"""
    def ls(self) -> List[str]:
        cwd = self.local.cwd
        with cwd.lock:
            if not cwd.is_directory:
                raise Exception("Current node is not a directory")
            
            # Check if we have read permission
            try:
                self.perm_manager.check_permission(cwd, "read")
                # Return empty list if no children
                if not cwd.children:
                    return []
                
                # Get list of children
                items = []
                for name, node in cwd.children.items():
                    # Add trailing slash for directories
                    if node.is_directory:
                        items.append(f"{name}/")
                    else:
                        items.append(name)
                
                # Return sorted list
                return sorted(items)
            except Exception:
                # If we have write permission but not read, we should still see the directory contents
                if self.local.user in cwd.permissions and cwd.permissions[self.local.user].write:
                    items = []
                    for name, node in cwd.children.items():
                        if node.is_directory:
                            items.append(f"{name}/")
                        else:
                            items.append(name)
                    return sorted(items)
                raise

    """Create a new directory"""
    def mkdir(self, name) -> FileSystemNode:
        # Handle absolute paths
        if name.startswith('/'):
            # Remove leading slash for node name
            name = name.lstrip('/')
            if not name:
                raise Exception("Cannot create root directory")
            
            # Split path into parts
            parts = name.split('/')
            current = self.root
            
            # Create each directory in the path
            for part in parts[:-1]:
                if part not in current.children:
                    node = FileSystemNode(part, owner=self.local.user, is_directory=True)
                    node.permissions[self.local.user] = Permission(owner=self.local.user, read=True, write=True)
                    current.add_child(node)
                current = current.children[part]
            
            # Create the final directory
            name = parts[-1]
            current = self._create_node(name, is_directory=True)
            return current
        else:
            # Create a single directory in the current working directory
            return self._create_node(name, is_directory=True)

    """Remove a directory"""
    def rmdir(self, name):
        cwd = self.local.cwd
        with cwd.lock:
            self.perm_manager.check_permission(cwd, "write")
            node = self._check_node_exists(name)
            if not node.is_directory:
                raise Exception(f"'{name}' is not a directory")
            if node.children:
                raise Exception("Directory is not empty")
            cwd.remove_child(name)

    """Move a directory"""
    def move(self, name, new_name):
        return super().move(name, new_name)

    """Change the current working directory"""
    def cd(self, path):
        if not path or path == "/":
            self.local.cwd = self.root
            return
        
        target = self._resolve_path(path)
        if not target:
            raise Exception(f"Directory '{path}' not found")
        if not target.is_directory:
            raise Exception(f"'{path}' is not a directory")
        
        # Check read permission
        self.perm_manager.check_permission(target, "read")
        
        # Update current working directory
        self.local.cwd = target
        
        # Print the new path
        print(f"Changed directory to: {self._get_path(target)}")

    """Resolve a path"""
    def _resolve_path(self, path):
        if not path or path == "/":
            return self.root
        parts = path.strip("/").split("/")
        current = self.root if path.startswith("/") else self.local.cwd
        for part in parts:
            if part == "..":
                if current.parent:
                    current = current.parent
                elif current == self.root:
                    continue
            elif part == "." or part == "":
                continue
            else:
                with current.lock:
                    if part not in current.children:
                        return None
                    current = current.children[part]
        return current

    def create_directory(self, path: str) -> None:
        """Create a new directory at the specified path"""
        # Handle root directory
        if path == "/":
            if not self.root:
                self.root = FileSystemNode("/", is_directory=True)
            return
            
        # Check for invalid path
        if not path or path.endswith("/") or "//" in path:
            raise Exception("Invalid path")
            
        parent_path = self.get_parent_path(path)
        
        # Create parent directories if they don't exist
        if parent_path != "/":
            try:
                self.get_node(parent_path)
            except Exception:
                self.create_directory(parent_path)
        
        # Get parent and create directory
        parent = self.get_node(parent_path)
        name = self.get_basename(path)
        
        if name in parent.children:
            raise ValueError(f"Directory {name} already exists")
            
        node = FileSystemNode(name, is_directory=True)
        parent.children[name] = node

    def list_directory(self, path: str) -> dict:
        """List contents of a directory"""
        node = self.get_node(path)
        if not node.is_directory:
            raise ValueError("Cannot list file as directory")
        return node.children

    def delete_directory(self, path: str, recursive: bool = False) -> None:
        """Delete a directory at the specified path"""
        if path == "/":
            raise ValueError("Cannot delete root directory")
            
        parent_path = self.get_parent_path(path)
        parent = self.get_node(parent_path)
        
        name = self.get_basename(path)
        if name not in parent.children:
            raise ValueError(f"Directory {name} not found")
            
        node = parent.children[name]
        if not node.is_directory:
            raise ValueError("Cannot delete file as directory")
            
        if not recursive and node.children:
            raise ValueError("Directory not empty")
            
        del parent.children[name]

    def move_directory(self, src_path: str, dst_path: str) -> None:
        """Move a directory from src_path to dst_path"""
        if src_path == "/":
            raise ValueError("Cannot move root directory")
            
        # Get source directory
        src_parent_path = self.get_parent_path(src_path)
        src_parent = self.get_node(src_parent_path)
        src_name = self.get_basename(src_path)
        
        if src_name not in src_parent.children:
            raise ValueError(f"Source directory {src_name} not found")
            
        src_node = src_parent.children[src_name]
        if not src_node.is_directory:
            raise ValueError("Cannot move file as directory")
            
        # Get destination
        dst_parent_path = self.get_parent_path(dst_path)
        dst_parent = self.get_node(dst_parent_path)
        dst_name = self.get_basename(dst_path)
        
        if dst_name in dst_parent.children:
            raise ValueError(f"Destination directory {dst_name} already exists")
            
        # Check if destination is subdirectory of source
        current = dst_parent
        while current != self.root:
            if current == src_node:
                raise ValueError("Cannot move directory to its subdirectory")
            current = self.get_node(self.get_parent_path(current.name))
            
        # Move directory
        dst_parent.children[dst_name] = src_node
        src_node.name = dst_name
        del src_parent.children[src_name] 