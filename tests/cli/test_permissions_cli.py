import pytest
from src.cli.permissions import PermissionsCLI, LocalState, PermissionManager

@pytest.fixture
def perms_cli():
    cli = PermissionsCLI()
    # Set up admin state for testing
    cli.local.user = "admin"
    cli.local.users = {"admin": "admin123"}
    cli.local.groups = {}
    cli.pm = PermissionManager(cli.local.cwd, cli.local)
    return cli

def test_user_management(perms_cli, capsys):
    # Create user
    perms_cli.set_user("testuser", "password123")
    
    # Login
    perms_cli.login("testuser", "password123")
    captured = capsys.readouterr()
    assert "Logged in as testuser" in captured.out
    
    # Delete user
    perms_cli.delete_user("testuser")
    
    # Try to login with deleted user
    perms_cli.login("testuser", "password123")
    captured = capsys.readouterr()
    assert "Error" in captured.out

def test_group_management(perms_cli, capsys):
    # Create user and group
    perms_cli.set_user("testuser", "password123")
    perms_cli.create_group("testgroup", read=True, write=True)
    perms_cli.add_to_group("testuser", "testgroup")
    capsys.readouterr()  # Clear output
    
    # List groups
    perms_cli.list_groups()
    captured = capsys.readouterr()
    assert "testgroup" in captured.out
    assert "testuser" in captured.out
    assert "Read: True" in captured.out
    assert "Write: True" in captured.out
    
    # Remove user from group
    perms_cli.remove_from_group("testuser", "testgroup")
    capsys.readouterr()  # Clear output
    
    # List groups again
    perms_cli.list_groups()
    captured = capsys.readouterr()
    assert "testgroup" in captured.out
    assert "testuser" not in captured.out
    
    # Delete group
    perms_cli.delete_group("testgroup")
    capsys.readouterr()  # Clear output
    
    # List groups one more time
    perms_cli.list_groups()
    captured = capsys.readouterr()
    assert "testgroup" not in captured.out

def test_node_permissions(perms_cli, capsys):
    # Create user
    perms_cli.set_user("testuser", "password123")
    
    # Set permissions
    perms_cli.set_perms("testfile", "testuser", "true", "false")
    capsys.readouterr()  # Clear output
    
    # List permissions
    perms_cli.list_perms("testfile")
    captured = capsys.readouterr()
    assert "testfile" in captured.out
    assert "testuser" in captured.out
    assert "read=True" in captured.out
    assert "write=False" in captured.out

def test_error_handling(perms_cli, capsys):
    # Test non-existent user operations
    perms_cli.delete_user("nonexistent")
    captured = capsys.readouterr()
    assert "Error" in captured.out
    
    # Test non-existent group operations
    perms_cli.delete_group("nonexistent")
    captured = capsys.readouterr()
    assert "Error" in captured.out
    
    # Test invalid group member operations
    perms_cli.add_to_group("nonexistent", "nonexistent")
    captured = capsys.readouterr()
    assert "Error" in captured.out

def test_admin_operations(perms_cli, capsys):
    # Try to delete admin user (should fail)
    perms_cli.delete_user("admin")
    captured = capsys.readouterr()
    assert "Error" in captured.out
    
    # Try to create admin user (should fail)
    perms_cli.set_user("admin", "password123")
    captured = capsys.readouterr()
    assert "Error" in captured.out

def test_group_permission_combinations(perms_cli, capsys):
    # Test different permission combinations
    perms_cli.create_group("readonly", read=True, write=False)
    perms_cli.create_group("writeonly", read=False, write=True)
    perms_cli.create_group("readwrite", read=True, write=True)
    perms_cli.create_group("noaccess", read=False, write=False)
    capsys.readouterr()  # Clear output
    
    perms_cli.list_groups()
    captured = capsys.readouterr()
    
    assert "readonly" in captured.out and "Read: True" in captured.out and "Write: False" in captured.out
    assert "writeonly" in captured.out and "Read: False" in captured.out and "Write: True" in captured.out
    assert "readwrite" in captured.out and "Read: True" in captured.out and "Write: True" in captured.out
    assert "noaccess" in captured.out and "Read: False" in captured.out and "Write: False" in captured.out 