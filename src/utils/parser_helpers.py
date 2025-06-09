import argparse

"""Create a parser for the filesys CLI"""
def create_filesys_parser():
    parser = argparse.ArgumentParser(description="File System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.add_parser('cd', help="Change directory")
    subparsers.add_parser('pwd', help="Print working directory")
    subparsers.add_parser('mkdir', help="Create directory")
    subparsers.add_parser('ls', help="List directory contents")
    subparsers.add_parser('rmdir', help="Remove directory")
    subparsers.add_parser('touch', help="Create file")
    subparsers.add_parser('write', help="Write to file")
    subparsers.add_parser('read', help="Read file")
    subparsers.add_parser('move', help="Move file or directory")
    subparsers.add_parser('find', help="Find files")
    return parser


"""Create a parser for the permissions CLI"""
def create_permissions_parser():
    parser = argparse.ArgumentParser(description="File System Permission Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # User management
    set_user_parser = subparsers.add_parser("set-user", help="Create a new user (admin only)")
    set_user_parser.add_argument("username", help="Username")
    set_user_parser.add_argument("password", help="Password")

    delete_user_parser = subparsers.add_parser("delete-user", help="Delete a user (admin only)")
    delete_user_parser.add_argument("username", help="Username to delete")

    login_parser = subparsers.add_parser("login", help="Login as a user")
    login_parser.add_argument("username", help="Username")
    login_parser.add_argument("password", help="Password")

    # Group management
    create_group_parser = subparsers.add_parser("create-group", help="Create a new permission group (admin only)")
    create_group_parser.add_argument("groupname", help="Group name")
    create_group_parser.add_argument("--read", action="store_true", help="Grant read permission")
    create_group_parser.add_argument("--write", action="store_true", help="Grant write permission")

    delete_group_parser = subparsers.add_parser("delete-group", help="Delete a permission group (admin only)")
    delete_group_parser.add_argument("groupname", help="Group name to delete")

    add_to_group_parser = subparsers.add_parser("add-to-group", help="Add a user to a group (admin only)")
    add_to_group_parser.add_argument("username", help="Username")
    add_to_group_parser.add_argument("groupname", help="Group name")

    remove_from_group_parser = subparsers.add_parser("remove-from-group", help="Remove a user from a group (admin only)")
    remove_from_group_parser.add_argument("username", help="Username")
    remove_from_group_parser.add_argument("groupname", help="Group name")

    # Node permissions
    set_perms_parser = subparsers.add_parser("set-perms", help="Set permissions for a node (admin only)")
    set_perms_parser.add_argument("name", help="Node name")
    set_perms_parser.add_argument("username", help="Target username")
    set_perms_parser.add_argument("read", type=lambda x: x.lower() == 'true', help="Read permission (true/false)")
    set_perms_parser.add_argument("write", type=lambda x: x.lower() == 'true', help="Write permission (true/false)")

    list_perms_parser = subparsers.add_parser("list-perms", help="List permissions for a node")
    list_perms_parser.add_argument("name", help="Node name")
    return parser