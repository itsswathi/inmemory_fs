import pytest

def test_create_file(file_ops, root_node):
    """Test creating a new file"""
    file_ops.create_file("/test.txt", "Hello World")
    
    # Check file exists
    assert "test.txt" in root_node.children
    assert root_node.children["test.txt"].content == "Hello World"
    assert not root_node.children["test.txt"].is_directory

def test_create_file_with_path(file_ops, dir_ops):
    """Test creating a file in a subdirectory"""
    # Create directory first
    dir_ops.create_directory("/testdir")
    
    # Create file in directory
    file_ops.create_file("/testdir/test.txt", "Hello World")
    
    # Check file exists in correct location
    node = file_ops.get_node("/testdir/test.txt")
    assert node.content == "Hello World"
    assert not node.is_directory

def test_create_file_invalid_path(file_ops):
    """Test creating a file in non-existent directory fails"""
    with pytest.raises(Exception):
        file_ops.create_file("/nonexistent/test.txt", "Hello World")

def test_read_file(file_ops):
    """Test reading file content"""
    # Create and read file
    file_ops.create_file("/test.txt", "Hello World")
    content = file_ops.read_file("/test.txt")
    
    assert content == "Hello World"

def test_read_nonexistent_file(file_ops):
    """Test reading non-existent file fails"""
    with pytest.raises(Exception):
        file_ops.read_file("/nonexistent.txt")

def test_write_file(file_ops):
    """Test writing to existing file"""
    # Create file
    file_ops.create_file("/test.txt", "Hello")
    
    # Write new content
    file_ops.write_file("/test.txt", "Hello World")
    
    # Verify content
    assert file_ops.read_file("/test.txt") == "Hello World"

def test_delete_file(file_ops, root_node):
    """Test deleting a file"""
    # Create and then delete file
    file_ops.create_file("/test.txt", "Hello World")
    file_ops.delete_file("/test.txt")
    
    # Verify file is gone
    assert "test.txt" not in root_node.children

def test_delete_nonexistent_file(file_ops):
    """Test deleting non-existent file fails"""
    with pytest.raises(Exception):
        file_ops.delete_file("/nonexistent.txt")

def test_move_file(file_ops, dir_ops):
    """Test moving a file"""
    # Setup
    file_ops.create_file("/test.txt", "Hello World")
    dir_ops.create_directory("/newdir")
    
    # Move file
    file_ops.move_file("/test.txt", "/newdir/test.txt")
    
    # Verify file moved
    assert file_ops.read_file("/newdir/test.txt") == "Hello World"
    with pytest.raises(Exception):
        file_ops.read_file("/test.txt") 