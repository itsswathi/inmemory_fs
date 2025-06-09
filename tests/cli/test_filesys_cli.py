import pytest
from src.cli.filesys import FileSystemCLI
from src.utils.models import Permission

@pytest.fixture
def fs_cli():
    cli = FileSystemCLI()
    # Set up root permissions
    cli.local.cwd.permissions["default_user"] = Permission(owner="default_user", read=True, write=True)
    return cli

def test_pwd(fs_cli, capsys):
    fs_cli.pwd()
    captured = capsys.readouterr()
    assert captured.out.strip() == "/"

def test_mkdir_and_ls(fs_cli, capsys):
    fs_cli.mkdir("test_dir")
    capsys.readouterr()  # Clear output
    
    fs_cli.ls()
    captured = capsys.readouterr()
    assert "test_dir" in captured.out

def test_cd_and_pwd(fs_cli, capsys):
    fs_cli.mkdir("test_dir")
    fs_cli.cd("test_dir")
    capsys.readouterr()  # Clear output
    
    fs_cli.pwd()
    captured = capsys.readouterr()
    assert captured.out.strip() == "/test_dir"

def test_touch_and_read(fs_cli, capsys):
    fs_cli.touch("test.txt")
    fs_cli.write("test.txt", "Hello, World!")
    capsys.readouterr()  # Clear output
    
    fs_cli.read("test.txt")
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out

def test_move_file(fs_cli, capsys):
    fs_cli.touch("old.txt")
    fs_cli.write("old.txt", "Test content")
    fs_cli.move(["old.txt", "new.txt"])
    capsys.readouterr()  # Clear output
    
    fs_cli.read("new.txt")
    captured = capsys.readouterr()
    assert "Test content" in captured.out
    
    fs_cli.ls()
    captured = capsys.readouterr()
    assert "new.txt" in captured.out
    assert "old.txt" not in captured.out

def test_rmdir(fs_cli, capsys):
    fs_cli.mkdir("test_dir")
    fs_cli.rmdir("test_dir")
    capsys.readouterr()  # Clear output
    
    fs_cli.ls()
    captured = capsys.readouterr()
    assert "test_dir" not in captured.out

def test_find(fs_cli, capsys):
    fs_cli.mkdir("dir1")
    fs_cli.cd("dir1")
    fs_cli.touch("test.txt")
    fs_cli.cd("/")
    fs_cli.mkdir("dir2")
    fs_cli.cd("dir2")
    fs_cli.touch("test.txt")
    fs_cli.cd("/")
    capsys.readouterr()  # Clear output
    
    fs_cli.find("test.txt")
    captured = capsys.readouterr()
    assert "/dir1/test.txt" in captured.out
    assert "/dir2/test.txt" in captured.out

def test_error_handling(fs_cli, capsys):
    # Test non-existent directory
    fs_cli.cd("nonexistent")
    captured = capsys.readouterr()
    assert "Error" in captured.out
    
    # Test non-existent file
    fs_cli.read("nonexistent.txt")
    captured = capsys.readouterr()
    assert "Error" in captured.out
    
    # Test invalid move operation
    fs_cli.move(["nonexistent.txt", "new.txt"])
    captured = capsys.readouterr()
    assert "Error" in captured.out 