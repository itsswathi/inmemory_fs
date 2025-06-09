from typing import Dict, Tuple
from src.utils.models import Permission, FileSystemNode

class NodePermissions:
    def __init__(self, root_node: FileSystemNode, local, users: Dict[str, str], groups):
        self.root = root_node
        self.local = local
        self.users = users
        self.groups = groups

    """Set direct permissions for a node (admin only)"""
    def set_permissions(self, node: FileSystemNode, target_user: str, read: bool = None, write: bool = None):
        self._check_admin()
            
        if target_user not in self.users:
            raise Exception("Target user not found")

        current_perm = node.permissions.get(target_user, Permission())
        if read is not None:
            current_perm.read = read
        if write is not None:
            current_perm.write = write
        node.permissions[target_user] = current_perm

    def list_permissions(self, node: FileSystemNode) -> Dict[str, Dict[str, Tuple[bool, bool]]]:
        # Combine direct permissions and group permissions
        effective_perms = {}
        
        # Add direct permissions
        for user, perm in node.permissions.items():
            effective_perms[user] = {"direct": (perm.read, perm.write)}

        # Add group permissions
        for groupname, group in self.groups.items():
            for member in group.members:
                if member not in effective_perms:
                    effective_perms[member] = {}
                effective_perms[member][f"via {groupname}"] = (group.read, group.write)

        return effective_perms

    """Check if current user has permission for an action"""
    def check_permission(self, node: FileSystemNode, action: str) -> bool:
        # Admin always has full access
        if self.local.user == "admin":
            return True
            
        # Node owner has full permissions
        if node.owner == self.local.user:
            return True

        # Check direct permissions
        direct_perms = node.permissions.get(self.local.user, Permission())
        if (action == "read" and direct_perms.read) or (action == "write" and direct_perms.write):
            return True

        # Check group permissions
        for group in self.groups.values():
            if self.local.user in group.members:
                if action == "read" and group.read:
                    return True
                if action == "write" and group.write:
                    return True

        raise PermissionError(f"{action.capitalize()} permission denied")

    """Recursively remove user's permissions from root node and its children"""
    def remove_user_permissions(self, username: str):
        self._remove_user_permissions_recursive(self.root, username)

    """Helper method to recursively remove user's permissions"""
    def _remove_user_permissions_recursive(self, node: FileSystemNode, username: str):
        if node.permissions and username in node.permissions:
            del node.permissions[username]
            
        if node.is_directory and node.children:
            for child in node.children.values():
                self._remove_user_permissions_recursive(child, username)

    """Check if current user is admin"""
    def _check_admin(self):
        if self.local.user != "admin":
            raise PermissionError("This operation requires admin privileges") 