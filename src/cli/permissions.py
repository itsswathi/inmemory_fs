#!/usr/bin/env python3

from src.permissions.permissions_manager import PermissionManager
from src.utils.models import FileSystemNode, Permission, LocalState
from src.utils.parser_helpers import create_permissions_parser
import os
import pickle

class PermissionsCLI:
    def __init__(self):
        # Load or initialize state
        try:
            with open(os.path.expanduser('~/.inmemory_fs_state.pkl'), 'rb') as f:
                self.local = pickle.load(f)
                if not self.local.cwd:
                    root = FileSystemNode("/", owner="admin", is_directory=True)
                    root.permissions["admin"] = Permission(owner="admin", read=True, write=True)
                    self.local.cwd = root
        except:
            # Initialize root node with proper permissions
            root = FileSystemNode("/", owner="admin", is_directory=True)
            root.permissions["admin"] = Permission(owner="admin", read=True, write=True)
            
            # Initialize local state with admin privileges and root directory
            self.local = LocalState(user="admin", cwd=root)
        
        # Initialize permissions manager
        self.pm = PermissionManager(self.local.cwd, self.local)

    def _save_state(self):
        with open(os.path.expanduser('~/.inmemory_fs_state.pkl'), 'wb') as f:
            pickle.dump(self.local, f)

    """Create a file if it doesn't exist"""
    def _ensure_file_exists(self, name):
        if name not in self.local.cwd.children:
            node = FileSystemNode(name, is_directory=False, owner=self.local.user)
            node.parent = self.local.cwd
            node.permissions[self.local.user] = Permission(owner=self.local.user, read=True, write=True)
            self.local.cwd.children[name] = node
            self._save_state()
        return self.local.cwd.children[name]

    """Create a new user (admin only)"""
    def set_user(self, username: str, password: str):
        try:
            self.pm.set_user(username, password)
            self._save_state()
            print(f"Created user: {username}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Delete a user (admin only)"""
    def delete_user(self, username: str):
        try:
            self.pm.delete_user(username)
            self._save_state()
            print(f"Deleted user: {username}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Login as a user"""
    def login(self, username: str, password: str):
        try:
            self.pm.login(username, password)
            self._save_state()
            print(f"Logged in as {username}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Create a new permission group (admin only)"""
    def create_group(self, groupname: str, read: bool = True, write: bool = False):
        try:
            self.pm.create_group(groupname, read, write)
            self._save_state()
            print(f"Created group: {groupname} (read={read}, write={write})")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Delete a permission group (admin only)"""
    def delete_group(self, groupname: str):
        try:
            self.pm.delete_group(groupname)
            self._save_state()
            print(f"Deleted group: {groupname}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Add a user to a group (admin only)"""
    def add_to_group(self, username: str, groupname: str):
        try:
            self.pm.add_user_to_group(username, groupname)
            self._save_state()
            print(f"Added {username} to group {groupname}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """Remove a user from a group (admin only)"""
    def remove_from_group(self, username: str, groupname: str):
        try:
            self.pm.remove_user_from_group(username, groupname)
            self._save_state()
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
    def set_perms(self, name: str, username: str, read: str, write: str):
        try:
            node = self._ensure_file_exists(name)
            # Convert string values to boolean
            read_bool = read.lower() == 'true'
            write_bool = write.lower() == 'true'
            self.pm.set_permissions(name, username, read_bool, write_bool)
            self._save_state()
            print(f"Set permissions for {name}: user={username}, read={read_bool}, write={write_bool}")
        except Exception as e:
            print(f"Error: {str(e)}")

    """List permissions for a node"""
    def list_perms(self, name: str):
        try:
            node = self._ensure_file_exists(name)
            perms = self.pm.list_permissions(name)
            print(f"\nPermissions for {name}:")
            for username, perm in perms.items():
                print(f"\nUser: {username}")
                print(f"  read={perm.read}, write={perm.write}")
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