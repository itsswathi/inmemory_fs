import pytest
from src.utils.models import FileSystemNode

def test_create_directory(dir_ops, root_node):
    """Test creating a new directory"""
    dir_ops.create_directory("/testdir")
    
    # Check directory exists
    assert "testdir" in root_node.children
    assert root_node.children["testdir"].is_directory

def test_create_nested_directory(dir_ops):
    """Test creating nested directories"""
    dir_ops.create_directory("/parent/child")
    
    # Verify path exists
    node = dir_ops.get_node("/parent/child")
    assert node.is_directory
    
    # Verify parent exists
    parent = dir_ops.get_node("/parent")
    assert parent.is_directory

def test_create_directory_invalid_path(dir_ops):
    """Test creating directory with invalid path fails"""
    with pytest.raises(Exception):
        dir_ops.create_directory("//invalid//path//")

def test_list_directory(dir_ops, file_ops):
    """Test listing directory contents"""
    # Create test structure
    dir_ops.create_directory("/testdir")
    file_ops.create_file("/testdir/test1.txt", "content1")
    file_ops.create_file("/testdir/test2.txt", "content2")
    dir_ops.create_directory("/testdir/subdir")
    
    # List contents
    contents = dir_ops.list_directory("/testdir")
    
    # Verify contents
    assert len(contents) == 3
    assert "test1.txt" in contents
    assert "test2.txt" in contents
    assert "subdir" in contents

def test_list_empty_directory(dir_ops):
    """Test listing empty directory"""
    dir_ops.create_directory("/emptydir")
    contents = dir_ops.list_directory("/emptydir")
    assert len(contents) == 0

def test_delete_directory(dir_ops, root_node):
    """Test deleting an empty directory"""
    # Create and delete directory
    dir_ops.create_directory("/testdir")
    dir_ops.delete_directory("/testdir")
    
    # Verify directory is gone
    assert "testdir" not in root_node.children

def test_delete_directory_recursive(dir_ops, file_ops):
    """Test deleting directory with contents"""
    # Create test structure
    dir_ops.create_directory("/testdir")
    file_ops.create_file("/testdir/test.txt", "content")
    dir_ops.create_directory("/testdir/subdir")
    
    # Delete directory
    dir_ops.delete_directory("/testdir", recursive=True)
    
    # Verify directory is gone
    with pytest.raises(Exception):
        dir_ops.get_node("/testdir")

def test_delete_directory_non_recursive(dir_ops, file_ops):
    """Test deleting non-empty directory without recursive fails"""
    # Create test structure
    dir_ops.create_directory("/testdir")
    file_ops.create_file("/testdir/test.txt", "content")
    
    # Attempt to delete
    with pytest.raises(Exception):
        dir_ops.delete_directory("/testdir", recursive=False)

def test_move_directory(dir_ops, file_ops):
    """Test moving a directory"""
    # Setup
    dir_ops.create_directory("/source")
    file_ops.create_file("/source/test.txt", "content")
    dir_ops.create_directory("/target")
    
    # Move directory
    dir_ops.move_directory("/source", "/target/source")
    
    # Verify move
    assert dir_ops.get_node("/target/source").is_directory
    assert file_ops.read_file("/target/source/test.txt") == "content"
    with pytest.raises(Exception):
        dir_ops.get_node("/source") 