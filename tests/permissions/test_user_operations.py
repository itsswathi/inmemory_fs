import pytest

def test_set_user(user_ops):
    """Test creating a new user"""
    user_ops.set_user("testuser", "password123")
    assert "testuser" in user_ops.users
    assert user_ops.users["testuser"] == "password123"

def test_set_user_no_password(user_ops):
    """Test creating user without password fails"""
    with pytest.raises(ValueError):
        user_ops.set_user("testuser", "")

def test_set_admin_fails(user_ops):
    """Test creating admin user fails"""
    with pytest.raises(PermissionError):
        user_ops.set_user("admin", "newpassword")

def test_delete_user(user_ops):
    """Test deleting a user"""
    # Create and delete user
    user_ops.set_user("testuser", "password123")
    user_ops.delete_user("testuser")
    assert "testuser" not in user_ops.users

def test_delete_nonexistent_user(user_ops):
    """Test deleting non-existent user fails"""
    with pytest.raises(ValueError):
        user_ops.delete_user("nonexistent")

def test_delete_admin_fails(user_ops):
    """Test deleting admin user fails"""
    with pytest.raises(PermissionError):
        user_ops.delete_user("admin")

def test_login_success(user_ops):
    """Test successful login"""
    user_ops.set_user("testuser", "password123")
    user_ops.login("testuser", "password123")
    assert user_ops.local.user == "testuser"

def test_login_wrong_password(user_ops):
    """Test login with wrong password fails"""
    user_ops.set_user("testuser", "password123")
    with pytest.raises(Exception):
        user_ops.login("testuser", "wrongpassword")

def test_login_nonexistent_user(user_ops):
    """Test login with non-existent user fails"""
    with pytest.raises(Exception):
        user_ops.login("nonexistent", "password123")

def test_admin_required(user_ops):
    """Test operations requiring admin privileges"""
    # Login as non-admin user
    user_ops.set_user("testuser", "password123")
    user_ops.login("testuser", "password123")
    
    # Attempt admin operations
    with pytest.raises(PermissionError):
        user_ops.set_user("newuser", "password")
    
    with pytest.raises(PermissionError):
        user_ops.delete_user("otheruser") 