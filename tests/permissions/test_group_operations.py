import pytest

def test_create_group(group_ops):
    """Test creating a new group"""
    group_ops.create_group("testgroup")
    assert "testgroup" in group_ops.groups
    assert group_ops.groups["testgroup"].read
    assert not group_ops.groups["testgroup"].write

def test_create_group_with_permissions(group_ops):
    """Test creating group with specific permissions"""
    group_ops.create_group("testgroup", read=True, write=True)
    assert group_ops.groups["testgroup"].read
    assert group_ops.groups["testgroup"].write

def test_create_existing_group(group_ops):
    """Test creating existing group fails"""
    group_ops.create_group("testgroup")
    with pytest.raises(ValueError):
        group_ops.create_group("testgroup")

def test_delete_group(group_ops):
    """Test deleting a group"""
    group_ops.create_group("testgroup")
    group_ops.delete_group("testgroup")
    assert "testgroup" not in group_ops.groups

def test_delete_nonexistent_group(group_ops):
    """Test deleting non-existent group fails"""
    with pytest.raises(ValueError):
        group_ops.delete_group("nonexistent")

def test_delete_admins_group(group_ops):
    """Test deleting admins group fails"""
    with pytest.raises(PermissionError):
        group_ops.delete_group("admins")

def test_add_user_to_group(group_ops, user_ops):
    """Test adding user to group"""
    # Setup
    user_ops.set_user("testuser", "password123")
    group_ops.create_group("testgroup")
    
    # Add user to group
    group_ops.add_user_to_group("testuser", "testgroup")
    assert "testuser" in group_ops.groups["testgroup"].members

def test_add_nonexistent_user(group_ops):
    """Test adding non-existent user fails"""
    group_ops.create_group("testgroup")
    with pytest.raises(ValueError):
        group_ops.add_user_to_group("nonexistent", "testgroup")

def test_add_user_to_nonexistent_group(group_ops, user_ops):
    """Test adding user to non-existent group fails"""
    user_ops.set_user("testuser", "password123")
    with pytest.raises(ValueError):
        group_ops.add_user_to_group("testuser", "nonexistent")

def test_remove_user_from_group(group_ops, user_ops):
    """Test removing user from group"""
    # Setup
    user_ops.set_user("testuser", "password123")
    group_ops.create_group("testgroup")
    group_ops.add_user_to_group("testuser", "testgroup")
    
    # Remove user
    group_ops.remove_user_from_group("testuser", "testgroup")
    assert "testuser" not in group_ops.groups["testgroup"].members

def test_remove_admin_from_admins(group_ops):
    """Test removing admin from admins group fails"""
    with pytest.raises(PermissionError):
        group_ops.remove_user_from_group("admin", "admins")

def test_list_groups(group_ops, user_ops):
    """Test listing groups"""
    # Setup
    user_ops.set_user("testuser", "password123")
    group_ops.create_group("testgroup", read=True, write=True)
    group_ops.add_user_to_group("testuser", "testgroup")
    
    # List groups
    groups = group_ops.list_groups()
    
    # Verify testgroup
    assert "testgroup" in groups
    assert groups["testgroup"]["read"]
    assert groups["testgroup"]["write"]
    assert "testuser" in groups["testgroup"]["members"]
    
    # Verify admins group
    assert "admins" in groups
    assert "admin" in groups["admins"]["members"] 