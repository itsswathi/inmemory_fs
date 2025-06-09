from typing import Dict
from dataclasses import dataclass
from typing import Set

@dataclass
class PermissionGroup:
    name: str
    read: bool = True
    write: bool = False
    members: Set[str] = None

    def __post_init__(self):
        if self.members is None:
            self.members = set()

class GroupOperations:
    def __init__(self, groups: Dict[str, PermissionGroup], users: Dict[str, str], local):
        self.groups = groups  # groupname -> PermissionGroup
        self.users = users
        self.local = local

    """Create a new permission group (admin only)"""
    def create_group(self, groupname: str, read: bool = True, write: bool = False):
        self._check_admin()

        if groupname in self.groups:
            raise ValueError(f"Group {groupname} already exists")

        self.groups[groupname] = PermissionGroup(groupname, read, write)

    """Delete a permission group (admin only)"""
    def delete_group(self, groupname: str):
        self._check_admin()

        if groupname not in self.groups:
            raise ValueError(f"Group {groupname} not found")
            
        if groupname == "admins":
            raise PermissionError("Cannot delete admins group")

        del self.groups[groupname]

    """Add a user to a group (admin only)"""
    def add_user_to_group(self, username: str, groupname: str):
        self._check_admin()

        if username not in self.users:
            raise ValueError(f"User {username} not found")
        if groupname not in self.groups:
            raise ValueError(f"Group {groupname} not found")

        self.groups[groupname].members.add(username)

    """Remove a user from a group (admin only)"""
    def remove_user_from_group(self, username: str, groupname: str):
        self._check_admin()

        if groupname not in self.groups:
            raise ValueError(f"Group {groupname} not found")
        if username == "admin" and groupname == "admins":
            raise PermissionError("Cannot remove admin from admins group")

        self.groups[groupname].members.discard(username)

    """List all permission groups and their members"""
    def list_groups(self):
        return {
            name: {
                "read": group.read,
                "write": group.write,
                "members": list(group.members)
            }
            for name, group in self.groups.items()
        }

    """Remove a user from all groups"""
    def remove_user_from_all_groups(self, username: str):
        for group in self.groups.values():
            group.members.discard(username)

    """Check if current user is admin"""
    def _check_admin(self):
        if self.local.user != "admin":
            raise PermissionError("This operation requires admin privileges") 