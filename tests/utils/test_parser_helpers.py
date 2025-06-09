import pytest
from src.utils.parser_helpers import create_filesys_parser, create_permissions_parser

def test_filesys_parser():
    parser = create_filesys_parser()
    
    # Test basic command parsing
    args = parser.parse_args(['cd', '/path'])
    assert args.command == 'cd'
    assert args.path == '/path'
    
    args = parser.parse_args(['pwd'])
    assert args.command == 'pwd'
    
    args = parser.parse_args(['mkdir', 'testdir'])
    assert args.command == 'mkdir'
    assert args.name == 'testdir'
    
    args = parser.parse_args(['ls'])
    assert args.command == 'ls'
    
    args = parser.parse_args(['rmdir', 'testdir'])
    assert args.command == 'rmdir'
    assert args.name == 'testdir'
    
    args = parser.parse_args(['touch', 'testfile'])
    assert args.command == 'touch'
    assert args.name == 'testfile'
    
    args = parser.parse_args(['write', 'testfile', 'content'])
    assert args.command == 'write'
    assert args.name == 'testfile'
    assert args.content == 'content'
    
    args = parser.parse_args(['read', 'testfile'])
    assert args.command == 'read'
    assert args.name == 'testfile'
    
    args = parser.parse_args(['move', 'source', 'dest'])
    assert args.command == 'move'
    assert args.source == 'source'
    assert args.destination == 'dest'
    
    args = parser.parse_args(['find', '*.txt'])
    assert args.command == 'find'
    assert args.pattern == '*.txt'

def test_permissions_parser():
    parser = create_permissions_parser()
    
    # Test user management commands
    args = parser.parse_args(['set-user', 'testuser', 'password123'])
    assert args.command == 'set-user'
    assert args.username == 'testuser'
    assert args.password == 'password123'
    
    args = parser.parse_args(['delete-user', 'testuser'])
    assert args.command == 'delete-user'
    assert args.username == 'testuser'
    
    args = parser.parse_args(['login', 'testuser', 'password123'])
    assert args.command == 'login'
    assert args.username == 'testuser'
    assert args.password == 'password123'
    
    # Test group management commands
    args = parser.parse_args(['create-group', 'testgroup', '--read', '--write'])
    assert args.command == 'create-group'
    assert args.groupname == 'testgroup'
    assert args.read is True
    assert args.write is True
    
    args = parser.parse_args(['create-group', 'testgroup'])
    assert args.command == 'create-group'
    assert args.groupname == 'testgroup'
    assert args.read is False
    assert args.write is False
    
    args = parser.parse_args(['delete-group', 'testgroup'])
    assert args.command == 'delete-group'
    assert args.groupname == 'testgroup'
    
    args = parser.parse_args(['add-to-group', 'testuser', 'testgroup'])
    assert args.command == 'add-to-group'
    assert args.username == 'testuser'
    assert args.groupname == 'testgroup'
    
    args = parser.parse_args(['remove-from-group', 'testuser', 'testgroup'])
    assert args.command == 'remove-from-group'
    assert args.username == 'testuser'
    assert args.groupname == 'testgroup'
    
    args = parser.parse_args(['list-groups'])
    assert args.command == 'list-groups'
    
    # Test node permission commands
    args = parser.parse_args(['set-perms', 'testfile', 'testuser', 'true', 'true'])
    assert args.command == 'set-perms'
    assert args.name == 'testfile'
    assert args.username == 'testuser'
    assert args.read == 'true'
    assert args.write == 'true'
    
    args = parser.parse_args(['list-perms', 'testfile'])
    assert args.command == 'list-perms'
    assert args.name == 'testfile'

def test_invalid_commands():
    filesys_parser = create_filesys_parser()
    perms_parser = create_permissions_parser()
    
    # Test invalid command handling
    with pytest.raises(SystemExit):
        filesys_parser.parse_args(['invalid-command'])
    
    with pytest.raises(SystemExit):
        perms_parser.parse_args(['invalid-command'])
    
    # Test missing required arguments
    with pytest.raises(SystemExit):
        perms_parser.parse_args(['set-user'])  # Missing username and password
    
    with pytest.raises(SystemExit):
        perms_parser.parse_args(['set-perms'])  # Missing all required arguments 