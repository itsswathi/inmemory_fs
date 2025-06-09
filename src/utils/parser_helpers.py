import argparse

"""Create a parser for the filesys CLI"""
def create_filesys_parser():
    parser = argparse.ArgumentParser(description="File System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add arguments for each command
    cd_parser = subparsers.add_parser('cd', help="Change directory")
    cd_parser.add_argument('path', help="Target directory path")
    
    subparsers.add_parser('pwd', help="Print working directory")
    
    mkdir_parser = subparsers.add_parser('mkdir', help="Create directory")
    mkdir_parser.add_argument('name', help="Directory name")
    
    subparsers.add_parser('ls', help="List directory contents")
    
    rmdir_parser = subparsers.add_parser('rmdir', help="Remove directory")
    rmdir_parser.add_argument('name', help="Directory name")
    
    touch_parser = subparsers.add_parser('touch', help="Create file")
    touch_parser.add_argument('name', help="File name")
    
    write_parser = subparsers.add_parser('write', help="Write to file")
    write_parser.add_argument('name', help="File name")
    write_parser.add_argument('content', help="Content to write")
    
    read_parser = subparsers.add_parser('read', help="Read file")
    read_parser.add_argument('name', help="File name")
    
    move_parser = subparsers.add_parser('move', help="Move/rename file or directory")
    move_parser.add_argument('source', help="Source name")
    move_parser.add_argument('destination', help="Destination name")
    
    find_parser = subparsers.add_parser('find', help="Find files/directories by pattern")
    find_parser.add_argument('pattern', help="Pattern to search for (supports glob patterns like *.txt)")
    
    return parser


"""Create a parser for the permissions CLI"""
def create_permissions_parser():
    parser = argparse.ArgumentParser(description='Manage filesystem permissions')
    subparsers = parser.add_subparsers(dest='command')

    # set-user command
    set_user_parser = subparsers.add_parser('set-user', help='Create or update a user')
    set_user_parser.add_argument('username', help='Username')
    set_user_parser.add_argument('password', help='Password')

    # delete-user command
    delete_user_parser = subparsers.add_parser('delete-user', help='Delete a user')
    delete_user_parser.add_argument('username', help='Username')

    # login command
    login_parser = subparsers.add_parser('login', help='Login as a user')
    login_parser.add_argument('username', help='Username')
    login_parser.add_argument('password', help='Password')

    # create-group command
    create_group_parser = subparsers.add_parser('create-group', help='Create a new group')
    create_group_parser.add_argument('groupname', help='Group name')
    create_group_parser.add_argument('--read', action='store_true', help='Grant read permission')
    create_group_parser.add_argument('--write', action='store_true', help='Grant write permission')

    # delete-group command
    delete_group_parser = subparsers.add_parser('delete-group', help='Delete a group')
    delete_group_parser.add_argument('groupname', help='Group name')

    # add-to-group command
    add_to_group_parser = subparsers.add_parser('add-to-group', help='Add a user to a group')
    add_to_group_parser.add_argument('username', help='Username')
    add_to_group_parser.add_argument('groupname', help='Group name')

    # remove-from-group command
    remove_from_group_parser = subparsers.add_parser('remove-from-group', help='Remove a user from a group')
    remove_from_group_parser.add_argument('username', help='Username')
    remove_from_group_parser.add_argument('groupname', help='Group name')

    # list-groups command
    subparsers.add_parser('list-groups', help='List all groups')

    # set-perms command
    set_perms_parser = subparsers.add_parser('set-perms', help='Set permissions for a file or directory')
    set_perms_parser.add_argument('name', help='File or directory name')
    set_perms_parser.add_argument('username', help='Username')
    set_perms_parser.add_argument('read', type=str, choices=['true', 'false'], help='Read permission (true/false)')
    set_perms_parser.add_argument('write', type=str, choices=['true', 'false'], help='Write permission (true/false)')

    # list-perms command
    list_perms_parser = subparsers.add_parser('list-perms', help='List permissions for a file or directory')
    list_perms_parser.add_argument('name', help='File or directory name')

    return parser