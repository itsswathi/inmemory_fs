from models import Permission, FileSystemNode
from typing import Dict, Set
from .user_operations import UserOperations
from .group_operations import GroupOperations, PermissionGroup
from .node_permissions import NodePermissions

class PermissionManager:
    def __init__(self, root_node: FileSystemNode, local, admin_password="admin123"):
        # Initialize state
        self.root = root_node
        self.local = local
        self.admin_password = admin_password
        self.users: Dict[str, str] = {"admin": self.admin_password}
        self.groups: Dict[str, PermissionGroup] = {}
        
        # Create default groups
        self.groups["readers"] = PermissionGroup("readers", read=True, write=False)
        self.groups["writers"] = PermissionGroup("writers", read=True, write=True)
        self.groups["admins"] = PermissionGroup("admins", read=True, write=True)
        self.groups["admins"].members.add("admin")

        # Initialize operations
        self.user_ops = UserOperations(self.users, self.local)
        self.group_ops = GroupOperations(self.groups, self.users, self.local)
        self.node_perms = NodePermissions(self.root, self.local, self.users, self.groups)

    # User operations
    """Create a new user (admin only)"""
    def set_user(self, username: str, password: str):
        self.user_ops.set_user(username, password)

    """Delete a user (admin only)"""
    def delete_user(self, username: str):
        self.user_ops.delete_user(username)
        self.group_ops.remove_user_from_all_groups(username)
        self.node_perms.remove_user_permissions(username)

    """Login as a user"""
    def login(self, username: str, password: str):
        self.user_ops.login(username, password)
        return Permission()

    # Group operations
    """Create a new permission group (admin only)"""
    def create_group(self, groupname: str, read: bool = True, write: bool = False):
        self.group_ops.create_group(groupname, read, write)

    """Delete a permission group (admin only)"""
    def delete_group(self, groupname: str):
        self.group_ops.delete_group(groupname)

    """Add a user to a group (admin only)"""
    def add_user_to_group(self, username: str, groupname: str):
        self.group_ops.add_user_to_group(username, groupname)

    """Remove a user from a group (admin only)"""
    def remove_user_from_group(self, username: str, groupname: str):
        self.group_ops.remove_user_from_group(username, groupname)

    """List all permission groups and their members"""
    def list_groups(self):
        return self.group_ops.list_groups()

    # Node permission operations
    """Set direct permissions for a node (admin only)"""
    def set_permissions(self, name: str, target_user: str, read: bool = None, write: bool = None):
        node = self._get_node(name)
        self.node_perms.set_permissions(node, target_user, read, write)

    """List permissions for a node"""
    def list_permissions(self, name: str):
        node = self._get_node(name)
        return self.node_perms.list_permissions(node)

    """Check if current user has permission for an action"""
    def check_permission(self, node, action: str):
        return self.node_perms.check_permission(node, action)

    """Helper to get a node by name from current directory"""
    def _get_node(self, name: str):
        node = self.local.cwd.children.get(name)
        if not node:
            raise Exception("Node not found")
        return node 