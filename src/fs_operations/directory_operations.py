from models import FileSystemNode, Permission
from node_operations import NodeOperations

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