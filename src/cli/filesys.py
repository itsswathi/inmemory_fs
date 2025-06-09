#!/usr/bin/env python3
from src.utils.models import FileSystemNode, Permission, LocalState
from src.fs_operations.file_operations import FileOperations
from src.fs_operations.node_operations import NodeOperations
from src.fs_operations.directory_operations import DirectoryOperations
from src.permissions.permissions_manager import PermissionManager
from src.utils.parser_helpers import create_filesys_parser
import os
import pickle

class FileSystemCLI:
    def __init__(self):
        # Load or initialize state
        try:
            with open(os.path.expanduser('~/.inmemory_fs_state.pkl'), 'rb') as f:
                self.local = pickle.load(f)
                # Ensure root node exists
                if not self.local.root:
                    root = FileSystemNode("/", owner="admin", is_directory=True)
                    root.permissions["admin"] = Permission(owner="admin", read=True, write=True)
                    self.local.root = root
                    self.local.cwd = root
                # Ensure cwd exists and has a valid path to root
                current = self.local.cwd
                while current and current != self.local.root:
                    if not current.parent:
                        # If we can't find a path to root, reset to root
                        self.local.cwd = self.local.root
                        break
                    current = current.parent
        except:
            # Initialize root node with proper permissions
            root = FileSystemNode("/", owner="admin", is_directory=True)
            root.permissions["admin"] = Permission(owner="admin", read=True, write=True)
            
            # Initialize local state with admin privileges and root directory
            self.local = LocalState(user="admin", cwd=root)
        
        # Initialize operations
        self.perm_manager = PermissionManager(self.local.root, self.local)
        self.node_ops = NodeOperations(self.local, self.perm_manager)
        self.dir_ops = DirectoryOperations(self.local, self.perm_manager)
        self.file_ops = FileOperations(self.local, self.perm_manager)

    def _save_state(self):
        with open(os.path.expanduser('~/.inmemory_fs_state.pkl'), 'wb') as f:
            pickle.dump(self.local, f)

    def _ensure_node_permissions(self, node):
        """Ensure node has proper permissions for the current user"""
        if self.local.user not in node.permissions:
            node.permissions[self.local.user] = Permission(owner=self.local.user, read=True, write=True)

    """Change directory"""
    def cd(self, path):
        try:
            self.dir_ops.cd(path)
            self._save_state()  # Save state after changing directory
        except Exception as e:
            print(f"Error: {str(e)}")

    """Print working directory"""
    def pwd(self):
        try:
            path = self.dir_ops.pwd()
            if path:
                print(path)
            else:
                print("/")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Create a new directory"""
    def mkdir(self, name):
        try:
            self._ensure_node_permissions(self.local.cwd)
            node = self.dir_ops.mkdir(name)
            print(f"Created directory: {name}")
            self._save_state()  # Save state after modification
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
            self._save_state()  # Save state after modification
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
            self._save_state()  # Save state after modification
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
            self._save_state()  # Save state after modification
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
            self._save_state()  # Save state after modification
        except Exception as e:
            print(f"Error: {str(e)}")

    """Find files/directories by pattern (supports glob patterns like *.txt)"""
    def find(self, pattern):
        try:
            self._ensure_node_permissions(self.local.cwd)
            results = self.file_ops._find_recursive(self.local.cwd, pattern)
            if results:
                print(f"Found matches for pattern '{pattern}' at:")
                for path in results:
                    print(f"  {path}")
            else:
                print(f"No items found matching pattern: {pattern}")
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    parser = create_filesys_parser()
    args = parser.parse_args()
    fs = FileSystemCLI()

    # Command mapping
    commands = {
        'cd': lambda: fs.cd(args.path),
        'pwd': lambda: fs.pwd(),
        'mkdir': lambda: fs.mkdir(args.name),
        'ls': lambda: fs.ls(),
        'rmdir': lambda: fs.rmdir(args.name),
        'touch': lambda: fs.touch(args.name),
        'write': lambda: fs.write(args.name, args.content),
        'read': lambda: fs.read(args.name),
        'move': lambda: fs.move(args.source, args.destination),
        'find': lambda: fs.find(args.pattern)
    }

    # Execute command
    if args.command:
        try:
            commands[args.command]()
        except AttributeError:
            print(f"Error: Missing required argument(s) for {args.command}")
            return
        except Exception as e:
            print(f"Error: {str(e)}")
            return
    else:
        parser.print_help()

if __name__ == "__main__":
    main()