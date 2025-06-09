from src.fs_operations.node_operations import NodeOperations
from src.models import FileSystemNode

"""
All directory operations supported by the filesystem
"""
class DirectoryOperations(NodeOperations):
    def __init__(self, root_node, local, perm_manager=None):
        super().__init__(root_node, local, perm_manager)

    """Get the current working directory"""
    def pwd(self):
        return super()._get_path(self.local.cwd)

    """List the contents of the current directory"""
    def ls(self):
        cwd = self.local.cwd
        with cwd.lock:
            self.perm_manager.check_permission(cwd, "read")
            if not cwd.is_directory:
                raise Exception("Current node is not a directory")
            return list(cwd.children.keys())

    """Create a new directory"""
    def mkdir(self, name):
        self._create_node(name, is_directory=True)

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
            del cwd.children[name]

    """Move a directory"""
    def move(self, name, new_name):
        return super().move(name, new_name)

    """Change the current working directory"""
    def cd(self, path):
        target = self._resolve_path(path)
        if not target or not target.is_directory:
            # TODO idea: if not present, offer an option to user to decide to create the directory chain
            raise Exception("Invalid path")
        self.perm_manager.check_permission(target, "read")
        self.local.cwd = target

    """Resolve a path"""
    def _resolve_path(self, path):
        parts = path.strip("/").split("/")
        current = self.root if path.startswith("/") else self.local.cwd
        for part in parts:
            if part == "..":
                if current.parent:
                    current = current.parent
            elif part == "." or part == "":
                continue
            else:
                with current.lock:
                    current = current.children.get(part)
                    if not current:
                        return None
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