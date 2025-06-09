# In-Memory File System

A Python-based in-memory file system implementation with support for file operations, directory management, and permissions.

## Features

### File Operations
- Create files with content
- Read file contents
- Write/update file contents
- Delete files
- Move files between directories

### Directory Operations
- Create directories (including nested directories)
- List directory contents
- Delete directories (with recursive option)
- Move directories

### Permission Management
- User Management
  - Create users
  - Delete users
  - User authentication (login)
- Group Management
  - Create permission groups
  - Delete groups
  - Add/remove users to/from groups
  - List groups and their members
- Node Permissions
  - Set read/write permissions for users
  - List permissions for nodes
  - Permission inheritance through groups

## Installation

1. Clone the repository:
```bash
git clone https://github.com/itsswathi/inmemory_fs.git
cd inmemory_fs
```

## Usage

### Docker
The project includes Docker support for easy deployment and isolation. The CLI commands (`fs` and `perms`) are automatically installed and available in the container.

#### Building and Running

Building the docker image also runs the unit tests

```bash
# Build Docker image
docker build -t inmemory-fs .

# Run container in interactive mode
docker run -it inmemory-fs

# Once inside the container, you can use the commands directly:
fs pwd           # Show current directory
fs mkdir /data   # Create a directory
fs touch /data/test.txt  # Create a file
perms set-user alice password123  # Create a user
```

#### Using Docker for Specific Commands

You can also run specific commands directly:

```bash
# Run a single fs command
docker run -it inmemory-fs fs ls /

# Run a single perms command
docker run -it inmemory-fs perms list-users

# Run with custom command
docker run -it inmemory-fs bash -c "fs mkdir /data && fs touch /data/test.txt"
```

Note that the filesystem is in-memory and container-specific. Data will be lost when the container stops. If you need to persist data between sessions, use the same container:

```bash
# Start container with a name
docker run -it --name my-fs inmemory-fs

# Later, restart and attach to the same container
docker start -ai my-fs
```

### Local virtual environment

#### Create a new virtual environment and activate
```bash
python3 -m venv venv
source venv/bin/activate  # On Unix/macOS
# OR
.\venv\Scripts\activate  # On Windows
```

#### Install the package (this will also install the CLI commands):
```bash
pip install -e .
```

After installation, the `fs` and `perms` commands will be available in your virtual environment. Make sure your virtual environment is activated before using these commands.

#### To verify the installation:
```bash
which fs    # On Unix/macOS
where fs    # On Windows
```

#### Running tests
```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run tests
python -m pytest -vv tests/
```

## Command Reference

The filesystem provides two main command-line tools:

1. `fs` - For file and directory operations
2. `perms` - For permission management

### File System CLI (`fs`)

The file system CLI provides the following commands for managing files and directories:

| Command | Arguments | Description | Example |
|---------|-----------|-------------|---------|
| `cd` | `<path>` | Change current directory | `fs cd /path/to/dir` |
| `pwd` | none | Print working directory | `fs pwd` |
| `mkdir` | `<name>` | Create a new directory | `fs mkdir newdir` |
| `ls` | none | List contents of current directory | `fs ls` |
| `rmdir` | `<name>` | Remove a directory (must be empty) | `fs rmdir olddir` |
| `touch` | `<name>` | Create a new empty file | `fs touch newfile.txt` |
| `write` | `<name> <content>` | Write content to a file | `fs write file.txt "Hello"` |
| `read` | `<name>` | Display file contents | `fs read file.txt` |
| `move` | `<old> <new>` | Move/rename file or directory | `fs move old.txt new.txt` |
| `find` | `<name>` | Find files/directories by name | `fs find *.txt` |

### Permissions CLI (`perms`)

The permissions CLI provides the following commands for managing users, groups, and permissions:

#### User Management

| Command | Arguments | Description | Example |
|---------|-----------|-------------|---------|
| `set-user` | `<username> <password>` | Create a new user | `perms set-user alice pass123` |
| `delete-user` | `<username>` | Delete an existing user | `perms delete-user alice` |
| `login` | `<username> <password>` | Login as a user | `perms login alice pass123` |

#### Group Management

| Command | Arguments | Description | Example |
|---------|-----------|-------------|---------|
| `create-group` | `<groupname> [--read] [--write]` | Create a new group | `perms create-group devs --read --write` |
| `delete-group` | `<groupname>` | Delete a group | `perms delete-group devs` |
| `add-to-group` | `<username> <groupname>` | Add user to group | `perms add-to-group alice devs` |
| `remove-from-group` | `<username> <groupname>` | Remove user from group | `perms remove-from-group alice devs` |
| `list-groups` | none | List all groups | `perms list-groups` |

#### Permission Management

| Command | Arguments | Description | Example |
|---------|-----------|-------------|---------|
| `set-perms` | `<name> <username> <read> <write>` | Set node permissions | `perms set-perms file.txt bob true false` |
| `list-perms` | `<name>` | List node permissions | `perms list-perms file.txt` |

### Notes

- Most permission management commands require admin privileges
- The default admin password is "admin123"
- Boolean values for permissions should be specified as 'true' or 'false'
- File and directory names should not contain spaces (use quotes if needed)
- Group permissions are inherited by all group members

## Development

### Project Structure

```
inmemory_fs/
├── src/                    # Source code
│   ├── cli/               # Command-line interface implementations
│   │   ├── filesys.py     # File system CLI
│   │   └── permissions.py # Permissions CLI
│   ├── fs_operations/     # Core file system operations
│   │   ├── node_operations.py    # Base operations for files/directories
│   │   ├── file_operations.py    # File-specific operations
│   │   └── directory_operations.py # Directory-specific operations
│   ├── permissions/       # Permission management system
│   │   ├── permissions_manager.py # Main permissions controller
│   │   ├── user_operations.py    # User management
│   │   ├── group_operations.py   # Group management
│   │   └── node_permissions.py   # Node-level permissions
│   └── utils/            # Utility functions and models
│       ├── models.py     # Data models (FileSystemNode, Permission)
│       └── parser_helpers.py # CLI argument parsers
├── tests/               # Test suite
│   ├── cli/            # CLI tests
│   ├── fs_operations/  # File system operation tests
│   ├── permissions/    # Permission system tests
│   └── utils/          # Utility function tests
├── setup.py            # Package installation configuration
├── requirements.txt    # Production dependencies
├── Dockerfile         # Docker configuration
└── README.md         # Project documentation
```

#### Key Components

1. **File System Operations**
   - `NodeOperations`: Base class for file/directory operations
   - `FileOperations`: File creation, reading, writing
   - `DirectoryOperations`: Directory creation, navigation, listing

2. **Permission System**
   - `PermissionManager`: Central permission controller
   - `UserOperations`: User account management
   - `GroupOperations`: Permission group management
   - `NodePermissions`: File/directory permission management

3. **Data Models**
   - `FileSystemNode`: Represents files and directories
   - `Permission`: Defines read/write permissions
   - `LocalState`: Manages current user and working directory

4. **Command Line Interfaces**
   - `FileSystemCLI`: File and directory operations
   - `PermissionsCLI`: User, group, and permission management

5. **Docker Support**
   - Containerized environment
   - Automated testing
   - Isolated runtime environment