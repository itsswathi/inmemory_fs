from typing import Dict
from dataclasses import dataclass, field
from typing import Set

@dataclass
class PermissionGroup:
    name: str
    read: bool = True
    write: bool = False
    members: Set[str] = field(default_factory=set)

    def __getstate__(self):
        return {
            'name': self.name,
            'read': self.read,
            'write': self.write,
            'members': self.members
        }

    def __setstate__(self, state):
        self.name = state['name']
        self.read = state['read']
        self.write = state['write']
        self.members = state['members']

class GroupOperations:
    """Operations for managing permission groups"""
    
    def __init__(self, groups: Dict[str, PermissionGroup], users: Dict[str, str], local):
        self.groups = groups
        self.users = users
        self.local = local

    def create_group(self, groupname: str, read: bool = True, write: bool = False):
        """Create a new permission group (admin only)"""
        if self.local.user != "admin":
            raise ValueError("Only admin can create groups")
            
        if groupname in self.groups:
            raise ValueError(f"Group {groupname} already exists")
            
        self.groups[groupname] = PermissionGroup(groupname, read, write)

    def delete_group(self, groupname: str):
        """Delete a permission group (admin only)"""
        if self.local.user != "admin":
            raise ValueError("Only admin can delete groups")
            
        if groupname == "admins":
            raise PermissionError("Cannot delete admins group")
            
        if groupname not in self.groups:
            raise ValueError(f"Group {groupname} not found")
            
        del self.groups[groupname]

    def add_user_to_group(self, username: str, groupname: str):
        """Add a user to a group (admin only)"""
        if self.local.user != "admin":
            raise ValueError("Only admin can modify group membership")
            
        if username not in self.users:
            raise ValueError(f"User {username} not found")
            
        if groupname not in self.groups:
            raise ValueError(f"Group {groupname} not found")
            
        self.groups[groupname].members.add(username)

    def remove_user_from_group(self, username: str, groupname: str):
        """Remove a user from a group (admin only)"""
        if self.local.user != "admin":
            raise ValueError("Only admin can modify group membership")
            
        if username == "admin" and groupname == "admins":
            raise PermissionError("Cannot remove admin from admins group")
            
        if groupname not in self.groups:
            raise ValueError(f"Group {groupname} not found")
            
        if username in self.groups[groupname].members:
            self.groups[groupname].members.remove(username)

    def remove_user_from_all_groups(self, username: str):
        """Remove a user from all groups"""
        for group in self.groups.values():
            if username in group.members:
                group.members.remove(username)

    def list_groups(self):
        """List all permission groups and their members"""
        return {
            name: {
                "read": group.read,
                "write": group.write,
                "members": list(group.members)
            }
            for name, group in self.groups.items()
        }

    """Check if current user is admin"""
    def _check_admin(self):
        if self.local.user != "admin":
            raise PermissionError("This operation requires admin privileges") 