from src.fs_operations.node_operations import NodeOperations
from src.utils.models import FileSystemNode

"""
All file operations supported by the filesystem
"""
class FileOperations(NodeOperations):
    def __init__(self, root_node, local, perm_manager=None):
        super().__init__(root_node, local, perm_manager)

    """Create a new file"""
    def touch(self, name):
        self._create_node(name, is_directory=False)

    """Write to a file"""
    def write(self, name, content):
        cwd = self.local.cwd
        with cwd.lock:
            file = self._check_node_exists(name)
            self.perm_manager.check_permission(file, "write")
            if file.is_directory:
                raise Exception(f"'{name}' is not a file")
            with file.lock:
                file.content = content

    """Read a file"""
    def read(self, name):
        cwd = self.local.cwd
        with cwd.lock:
            file = self._check_node_exists(name)
            self.perm_manager.check_permission(file, "read")
            if file.is_directory:
                raise Exception(f"'{name}' is not a file")
            with file.lock:
                return file.content

    """Move a file"""
    def move(self, name, new_name):
        return super().move(name, new_name)

    """Find a file"""
    def find(self, name):
        return super().find(name)

    def create_file(self, path: str, content: str = "") -> None:
        """Create a new file at the specified path"""
        parent_path = self.get_parent_path(path)
        parent = self.get_node(parent_path)
        
        if not parent.is_directory:
            raise ValueError("Parent must be a directory")
            
        name = self.get_basename(path)
        if name in parent.children:
            raise ValueError(f"File {name} already exists")
            
        node = FileSystemNode(name, is_directory=False)
        node.content = content
        parent.children[name] = node

    def read_file(self, path: str) -> str:
        """Read the contents of a file"""
        node = self.get_node(path)
        if node.is_directory:
            raise ValueError("Cannot read directory as file")
        return node.content

    def write_file(self, path: str, content: str) -> None:
        """Write content to a file, creating it if it doesn't exist"""
        try:
            node = self.get_node(path)
            if node.is_directory:
                raise ValueError("Cannot write to directory")
            node.content = content
        except Exception:
            self.create_file(path, content)

    def delete_file(self, path: str) -> None:
        """Delete a file at the specified path"""
        parent_path = self.get_parent_path(path)
        parent = self.get_node(parent_path)
        
        name = self.get_basename(path)
        if name not in parent.children:
            raise ValueError(f"File {name} not found")
            
        node = parent.children[name]
        if node.is_directory:
            raise ValueError("Cannot delete directory as file")
            
        del parent.children[name]

    def move_file(self, src_path: str, dst_path: str) -> None:
        """Move a file from src_path to dst_path"""
        # Get source file
        src_parent_path = self.get_parent_path(src_path)
        src_parent = self.get_node(src_parent_path)
        src_name = self.get_basename(src_path)
        
        if src_name not in src_parent.children:
            raise ValueError(f"Source file {src_name} not found")
            
        src_node = src_parent.children[src_name]
        if src_node.is_directory:
            raise ValueError("Cannot move directory as file")
            
        # Get destination
        dst_parent_path = self.get_parent_path(dst_path)
        dst_parent = self.get_node(dst_parent_path)
        dst_name = self.get_basename(dst_path)
        
        if dst_name in dst_parent.children:
            raise ValueError(f"Destination file {dst_name} already exists")
            
        # Move file
        dst_parent.children[dst_name] = src_node
        src_node.name = dst_name
        del src_parent.children[src_name]
        