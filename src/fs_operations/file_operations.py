from node_operations import NodeOperations

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
        