#!/usr/bin/env python3

from src.permissions.permissions_manager import PermissionManager
from src.utils.models import FileSystemNode, Permission
from dataclasses import dataclass
from src.utils.parser_helpers import create_permissions_parser

@dataclass
class LocalState:
    user: str = "default_user"
    cwd: FileSystemNode = None

class PermissionsCLI:
    def __init__(self):
        # Initialize root node with proper permissions
        root = FileSystemNode("/", owner="admin", is_directory=True)
        root.permissions["admin"] = Permission(owner="admin", read=True, write=True)
        
        # Initialize local state with admin privileges and root directory
        self.local = LocalState(user="admin", cwd=root)
        
        # Initialize permissions manager
        self.pm = PermissionManager(root, self.local)

    """Create a file if it doesn't exist"""
    def _ensure_file_exists(self, name):
        if name not in self.local.cwd.children:
            node = FileSystemNode(name, is_directory=False, owner=self.local.user)
            node.parent = self.local.cwd
            node.permissions[self.local.user] = Permission(owner=self.local.user, read=True, write=True)
            self.local.cwd.children[name] = node
        return self.local.cwd.children[name]

    """Create a new user (admin only)"""
    def set_user(self, username: str, password: str):
        try:
            self.pm.set_user(username, password)
            print(f"Created user: {username}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Delete a user (admin only)"""
    def delete_user(self, username: str):
        try:
            self.pm.delete_user(username)
            print(f"Deleted user: {username}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Login as a user"""
    def login(self, username: str, password: str):
        try:
            self.pm.login(username, password)
            print(f"Logged in as {username}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Create a new permission group (admin only)"""
    def create_group(self, groupname: str, read: bool = True, write: bool = False):
        try:
            self.pm.create_group(groupname, read, write)
            print(f"Created group: {groupname} (read={read}, write={write})")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Delete a permission group (admin only)"""
    def delete_group(self, groupname: str):
        try:
            self.pm.delete_group(groupname)
            print(f"Deleted group: {groupname}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Add a user to a group (admin only)"""
    def add_to_group(self, username: str, groupname: str):
        try:
            self.pm.add_user_to_group(username, groupname)
            print(f"Added {username} to group {groupname}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Remove a user from a group (admin only)"""
    def remove_from_group(self, username: str, groupname: str):
        try:
            self.pm.remove_user_from_group(username, groupname)
            print(f"Removed {username} from group {groupname}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """List all permission groups"""
    def list_groups(self):
        try:
            groups = self.pm.list_groups()
            for name, info in groups.items():
                print(f"\nGroup: {name}")
                print(f"  Read: {info['read']}")
                print(f"  Write: {info['write']}")
                print(f"  Members: {', '.join(info['members']) if info['members'] else 'None'}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Set permissions for a node (admin only)"""
    def set_perms(self, name: str, username: str, read: bool, write: bool):
        try:
            node = self._ensure_file_exists(name)
            self.pm.set_permissions(name, username, read, write)
            print(f"Set permissions for {name}: user={username}, read={read}, write={write}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """List permissions for a node"""
    def list_perms(self, name: str):
        try:
            node = self._ensure_file_exists(name)
            perms = self.pm.list_permissions(name)
            print(f"\nPermissions for {name}:")
            for user, sources in perms.items():
                print(f"\nUser: {user}")
                for source, (read, write) in sources.items():
                    print(f"  {source}: read={read}, write={write}")
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    parser = create_permissions_parser()
    args = parser.parse_args()
    cli = PermissionsCLI()

    # Command mapping
    commands = {
        'set-user': lambda: cli.set_user(args.username, args.password),
        'delete-user': lambda: cli.delete_user(args.username),
        'login': lambda: cli.login(args.username, args.password),
        'create-group': lambda: cli.create_group(args.groupname, args.read, args.write),
        'delete-group': lambda: cli.delete_group(args.groupname),
        'add-to-group': lambda: cli.add_to_group(args.username, args.groupname),
        'remove-from-group': lambda: cli.remove_from_group(args.username, args.groupname),
        'list-groups': lambda: cli.list_groups(),
        'set-perms': lambda: cli.set_perms(args.name, args.username, args.read, args.write),
        'list-perms': lambda: cli.list_perms(args.name)
    }

    # Argument validation
    required_args = {
        'set-user': 2, 'delete-user': 1, 'login': 2,
        'create-group': 1, 'delete-group': 1,
        'add-to-group': 2, 'remove-from-group': 2, 'list-groups': 0,
        'set-perms': 4, 'list-perms': 1
    }

    if args.command:
        if len(args.args) < required_args[args.command]:
            print(f"Error: {args.command} requires {required_args[args.command]} argument(s)")
            return

        # Execute command
        commands[args.command]()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 