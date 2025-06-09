#!/usr/bin/env python3
from models import FileSystemNode, Permission
from src.fs_operations.file_operations import FileOperations
from src.fs_operations.directory_operations import DirectoryOperations
from dataclasses import dataclass
from src.utils.parser_helpers import create_filesys_parser

@dataclass
class LocalState:
    cwd: FileSystemNode
    user: str = "default_user"

class FileSystemCLI:
    def __init__(self):
        # Initialize root node
        self.root = FileSystemNode("/", owner="default_user")
        self.root.permissions["default_user"] = Permission()
        
        # Initialize local state
        self.local = LocalState(cwd=self.root)
        
        # Initialize operations
        self.file_ops = FileOperations(self.root, self.local)
        self.dir_ops = DirectoryOperations(self.root, self.local)

    """Change directory"""
    def cd(self, path):
        try:
            self.dir_ops.cd(path)
            print(f"Changed directory to: {self.dir_ops.pwd()}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Print working directory"""
    def pwd(self):
        try:
            print(self.dir_ops.pwd())
        except Exception as e:
            print(f"Error: {str(e)}")

    """Create a new directory"""
    def mkdir(self, name):
        try:
            self.dir_ops.mkdir(name)
            print(f"Created directory: {name}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """List directory contents"""
    def ls(self):
        try:
            contents = self.dir_ops.ls()
            print(contents)
        except Exception as e:
            print(f"Error: {str(e)}")

    """Remove a directory"""
    def rmdir(self, name):
        try:
            self.dir_ops.rmdir(name)
            print(f"Removed directory: {name}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Create a new file"""
    def touch(self, name):
        try:
            self.file_ops.touch(name)
            print(f"Created file: {name}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Write to a file"""
    def write(self, name, content):
        try:
            self.file_ops.write(name, content)
            print(f"Wrote to file: {name}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Read from a file"""
    def read(self, name):
        try:
            content = self.file_ops.read(name)
            print(f"Content of {name}:")
            print(content)
        except Exception as e:
            print(f"Error: {str(e)}")

    """Move/rename a file"""
    def move(self, name, new_name):
        try:
            self.file_ops.move(name, new_name)
            print(f"Moved {name} to {new_name}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Find files/directories by name"""
    def find(self, name):
        try:
            results = self.file_ops.find(name)
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