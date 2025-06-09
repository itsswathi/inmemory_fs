#!/usr/bin/env python3
from src.utils.models import FileSystemNode, Permission
from src.fs_operations.file_operations import FileOperations
from src.fs_operations.directory_operations import DirectoryOperations
from src.permissions.permissions_manager import PermissionManager
from dataclasses import dataclass
from src.utils.parser_helpers import create_filesys_parser

@dataclass
class LocalState:
    cwd: FileSystemNode
    user: str = "default_user"

class FileSystemCLI:
    def __init__(self):
        # Initialize root node
        self.root = FileSystemNode("/", owner="default_user", is_directory=True)
        self.root.permissions["default_user"] = Permission(owner="default_user", read=True, write=True)
        
        # Initialize local state
        self.local = LocalState(cwd=self.root)
        
        # Initialize permission manager
        self.perm_manager = PermissionManager(self.root, self.local)
        
        # Initialize operations
        self.file_ops = FileOperations(self.root, self.local, self.perm_manager)
        self.dir_ops = DirectoryOperations(self.root, self.local, self.perm_manager)

    def _ensure_node_permissions(self, node):
        """Ensure node has proper permissions for the current user"""
        if self.local.user not in node.permissions:
            node.permissions[self.local.user] = Permission(owner=self.local.user, read=True, write=True)

    """Change directory"""
    def cd(self, path):
        try:
            target = self.dir_ops.get_node(path)
            if target:
                self._ensure_node_permissions(target)
            self.dir_ops.cd(path)
            print(f"Changed directory to: {self.dir_ops.pwd()}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Print working directory"""
    def pwd(self):
        try:
            path = self.dir_ops.pwd()
            print(path)
        except Exception as e:
            print(f"Error: {str(e)}")

    """Create a new directory"""
    def mkdir(self, name):
        try:
            self._ensure_node_permissions(self.local.cwd)
            self.dir_ops.mkdir(name)
            new_dir = self.dir_ops.get_node(name)
            if new_dir:
                self._ensure_node_permissions(new_dir)
            print(f"Created directory: {name}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """List directory contents"""
    def ls(self):
        try:
            self._ensure_node_permissions(self.local.cwd)
            contents = self.dir_ops.ls()
            if contents:
                print("\n".join(contents))
            else:
                print("Directory is empty")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Remove a directory"""
    def rmdir(self, name):
        try:
            self._ensure_node_permissions(self.local.cwd)
            target = self.dir_ops.get_node(name)
            if target:
                self._ensure_node_permissions(target)
            self.dir_ops.rmdir(name)
            print(f"Removed directory: {name}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Create a new file"""
    def touch(self, name):
        try:
            self._ensure_node_permissions(self.local.cwd)
            self.file_ops.touch(name)
            new_file = self.file_ops.get_node(name)
            if new_file:
                self._ensure_node_permissions(new_file)
            print(f"Created file: {name}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Write to a file"""
    def write(self, name, content):
        try:
            self._ensure_node_permissions(self.local.cwd)
            target = self.file_ops.get_node(name)
            if target:
                self._ensure_node_permissions(target)
            self.file_ops.write(name, content)
            print(f"Wrote to file: {name}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Read from a file"""
    def read(self, name):
        try:
            self._ensure_node_permissions(self.local.cwd)
            target = self.file_ops.get_node(name)
            if target:
                self._ensure_node_permissions(target)
            content = self.file_ops.read(name)
            print(f"Content of {name}:")
            print(content)
        except Exception as e:
            print(f"Error: {str(e)}")

    """Move/rename a file"""
    def move(self, name, new_name):
        try:
            self._ensure_node_permissions(self.local.cwd)
            source = self.file_ops.get_node(name)
            if source:
                self._ensure_node_permissions(source)
            self.file_ops.move(name, new_name)
            target = self.file_ops.get_node(new_name)
            if target:
                self._ensure_node_permissions(target)
            print(f"Moved {name} to {new_name}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Find files/directories by name"""
    def find(self, name):
        try:
            self._ensure_node_permissions(self.local.cwd)
            results = self.file_ops._find_recursive(self.local.cwd, name)
            if results:
                print(f"Found {name} at:")
                for path in results:
                    print(f"  {path}")
            else:
                print(f"No items found with name: {name}")
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    parser = create_filesys_parser()
    args = parser.parse_args()
    fs = FileSystemCLI()

    # Command mapping
    commands = {
        'cd': lambda: fs.cd(args.args[0]),
        'pwd': lambda: fs.pwd(),
        'mkdir': lambda: fs.mkdir(args.args[0]),
        'ls': lambda: fs.ls(),
        'rmdir': lambda: fs.rmdir(args.args[0]),
        'touch': lambda: fs.touch(args.args[0]),
        'write': lambda: fs.write(args.args[0], args.args[1]),
        'read': lambda: fs.read(args.args[0]),
        'move': lambda: fs.move(args.args[0], args.args[1]),
        'find': lambda: fs.find(args.args[0])
    }

    # Argument validation
    required_args = {
        'cd': 1, 'pwd': 0, 'mkdir': 1, 'ls': 0, 'rmdir': 1,
        'touch': 1, 'write': 2, 'read': 1, 'move': 2, 'find': 1
    }

    # Execute command
    if args.command:
        if len(args.args) < required_args[args.command]:
            print(f"Error: {args.command} requires {required_args[args.command]} argument(s)")
            return
        commands[args.command]()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()