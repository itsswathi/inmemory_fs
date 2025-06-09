from typing import Dict

class UserOperations:
    def __init__(self, users: Dict[str, str], local):
        self.users = users  # username -> password
        self.local = local

    """Create a new user (admin only)"""
    def set_user(self, username: str, password: str):
        self._check_admin()
            
        if username == "admin":
            raise PermissionError("Cannot modify admin user")
            
        if not password:
            raise ValueError("Password is required")
            
        self.users[username] = password

    """Delete a user (admin only)"""
    def delete_user(self, username: str):
        self._check_admin()

        if username == "admin":
            raise PermissionError("Cannot delete admin user")
            
        if username not in self.users:
            raise ValueError(f"User {username} not found")
            
        del self.users[username]

    """Login as a user"""
    def login(self, username: str, password: str):
        if username not in self.users:
            raise Exception("User not found")
        if self.users[username] != password:
            raise Exception("Invalid password")
            
        self.local.user = username

    """Check if current user is admin"""
    def _check_admin(self):
        if self.local.user != "admin":
            raise PermissionError("This operation requires admin privileges") 