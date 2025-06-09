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

| Command | Arguments | Description | Examples |
|---------|-----------|-------------|----------|
| `cd` | `<path>` | Change current directory. Supports absolute paths, relative paths, parent dir (..), and home dir (~) | `fs cd /home/user`<br>`fs cd ..`<br>`fs cd ../sibling/dir`<br>`fs cd ~/projects`<br>`fs cd ../../parent/other` |
| `pwd` | none | Shows absolute path from root. | `fs pwd`<br>`fs pwd > path.txt`<br>`fs pwd && ls` |
| `mkdir` | `<name>` | Create a new directory. Creates parent directories with -p flag. Supports absolute/relative paths | `fs mkdir projects`<br>`fs mkdir -p src/main/java`<br>`fs mkdir ../shared/docs`<br>`fs mkdir /home/user/data`<br>`fs mkdir backup_$(date +%Y%m%d)` |
| `ls` | none | List contents of current directory | `fs ls`<br>`fs ls /home/user`<br>`fs ls ../other`<br>`fs ls /var/log`<br>`fs ls ~/projects` |
| `rmdir` | `<name>` | Remove a directory. Use -r for non-empty dirs. | `fs rmdir empty_dir`<br>`fs rmdir -r project_old`<br>`fs rmdir ../temp`<br>`fs rmdir /home/user/old_data`<br>`fs rmdir -r test_*` |
| `touch` | `<name>` | Create a new empty file. Creates parent dirs if needed. | `fs touch README.md`<br>`fs touch src/main.py`<br>`fs touch .env.local`<br>`fs touch logs/app.log`<br>`fs touch data/{1..5}.txt` |
| `write` | `<name> <content>` | Write content to a file. Overwrites existing content. Use quotes for content with spaces | `fs write config.json '{"port": 8080}'`<br>`fs write .env "API_KEY=xyz123"`<br>`fs write logs/error.log "Failed to connect"`<br>`fs write src/version.txt "v1.0.0"`<br>`fs write data.csv "id,name,value"` |
| `read` | `<name>` | Display file contents. Requires read permission. Works with any text file | `fs read config.json`<br>`fs read .env.local`<br>`fs read logs/latest.log`<br>`fs read src/main.py`<br>`fs read ~/projects/README.md` |
| `move` | `<source> <dest>` | Move/rename file or directory. Works with files and dirs. Supports patterns. Preserves permissions | `fs move old.txt new.txt`<br>`fs move src/* /backup/`<br>`fs move *.log logs/`<br>`fs move project_v1 project_v2`<br>`fs move /tmp/file.txt ~/docs/` |
| `find` | `<pattern>` | Find files/directories by pattern | `fs find *.py`<br>`fs find test_*.js`<br>`fs find *.{jpg,png,gif}`<br>`fs find data/*.csv`<br>`fs find src/**/*.java` |

### Common File System Scenarios

1. **Project Setup**
```bash
# Create project structure
fs mkdir -p myproject/{src,tests,docs,config}
fs touch myproject/README.md
fs write myproject/README.md "# My Project\n\nDescription here"
fs touch myproject/config/settings.json
fs write myproject/config/settings.json '{"env": "dev"}'

# Create source files
fs touch myproject/src/main.py
fs touch myproject/src/utils.py
fs touch myproject/tests/test_main.py
```

2. **Log Management**
```bash
# Set up log directory
fs mkdir -p logs/{app,error,access}
fs touch logs/app/current.log
fs touch logs/error/errors.log
fs touch logs/access/requests.log

# Rotate logs
fs move logs/app/current.log logs/app/$(date +%Y%m%d).log
fs touch logs/app/current.log
```

3. **Configuration Management**
```bash
# Create config hierarchy
fs mkdir -p config/{dev,prod,stage}
fs write config/dev/.env "DEBUG=true\nPORT=3000"
fs write config/prod/.env "DEBUG=false\nPORT=80"
fs write config/stage/.env "DEBUG=true\nPORT=8080"

# Create shared config
fs write config/common.json '{"version": "1.0.0"}'
```

4. **Backup and Restore**
```bash
# Create backup structure
fs mkdir -p backup/$(date +%Y%m%d)
fs move src/* backup/$(date +%Y%m%d)/
fs mkdir src
fs move backup/$(date +%Y%m%d)/* src/
```

5. **Working with Multiple Files**
```bash
# Create multiple related files
fs mkdir -p data/users
fs touch data/users/{config,schema,types}.ts
fs write data/users/config.ts "export const config = {}"
fs write data/users/schema.ts "export const schema = {}"
fs write data/users/types.ts "export type User = {}"

# Organize files by type
fs mkdir -p src/{components,hooks,utils}
fs move src/*.tsx src/components/
fs move src/*.hook.ts src/hooks/
fs move src/*.util.ts src/utils/
```

### Permissions CLI (`perms`)

The permissions CLI provides comprehensive user, group, and permission management:

#### User Management

| Command | Arguments | Description | Examples |
|---------|-----------|-------------|----------|
| `set-user` | `<username> <password>` | Create a new user, Cannot create 'admin' user | `perms set-user alice pass123`<br>`perms set-user bob "secure pwd!"`<br>`perms set-user developer dev@2024`<br>`perms set-user guest temp123`<br>`perms set-user jenkins jenkins@ci` |
| `delete-user` | `<username>` | Delete an existing user, Admin only. Cannot delete 'admin' user | `perms delete-user alice`<br>`perms delete-user temp_user`<br>`perms delete-user old_employee`<br>`perms delete-user guest` |
| `login` | `<username> <password>` | Login as a user. Changes current user context | `perms login alice pass123`<br>`perms login admin admin123`<br>`perms login developer dev@2024`<br>`perms login jenkins jenkins@ci` |

#### Group Management

| Command | Arguments | Description | Examples |
|---------|-----------|-------------|----------|
| `create-group` | `<groupname> [--read] [--write]` | Create a new group, Admin only. Default: read-only | `perms create-group devs --read --write`<br>`perms create-group readers --read`<br>`perms create-group admins --read --write`<br>`perms create-group qa --read`<br>`perms create-group deploy --read --write` |
| `delete-group` | `<groupname>` | Delete a group, Admin only. Cannoy delete 'admins' group | `perms delete-group temp_group`<br>`perms delete-group old_team`<br>`perms delete-group project_x`<br>`perms delete-group test_group` |
| `add-to-group` | `<username> <groupname>` | Add user to group, Admin only. User must exist | `perms add-to-group alice devs`<br>`perms add-to-group bob readers`<br>`perms add-to-group carol admins`<br>`perms add-to-group dave qa`<br>`perms add-to-group eve deploy` |
| `remove-from-group` | `<username> <groupname>` | Remove user from group, Admin only. Cannot remove admin from admins | `perms remove-from-group alice devs`<br>`perms remove-from-group bob readers`<br>`perms remove-from-group carol qa`<br>`perms remove-from-group dave deploy` |
| `list-groups` | none | List all groups, Shows members and permissions | `perms list-groups` |

#### Permission Management

| Command | Arguments | Description | Examples |
|---------|-----------|-------------|----------|
| `set-perms` | `<name> <username> <read> <write>` | Set node permissions, Admin only. Use 'true'/'false' | `perms set-perms file.txt bob true false`<br>`perms set-perms config.json alice true true`<br>`perms set-perms scripts/ carol true true`<br>`perms set-perms logs/ dave true false`<br>`perms set-perms .env eve false false` |
| `list-perms` | `<name>` | List node permissions | `perms list-perms file.txt`<br>`perms list-perms /home/user`<br>`perms list-perms config/`<br>`perms list-perms .gitignore` |

### Common Permission Scenarios

Here are some common scenarios and the commands to achieve them:

1. **Setting up a new developer**
```bash
# Create user and add to groups
perms set-user dev1 "pass123"
perms add-to-group dev1 developers
perms add-to-group dev1 readers

# Set specific permissions
perms set-perms src/ dev1 true true
perms set-perms tests/ dev1 true true
perms set-perms config/ dev1 true false
```

2. **Creating a read-only user**
```bash
# Create user with limited access
perms set-user auditor "audit@2024"
perms add-to-group auditor readers
perms set-perms logs/ auditor true false
perms set-perms reports/ auditor true false
```

3. **Setting up project permissions**
```bash
# Create project group
perms create-group project_x --read --write

# Add team members
perms add-to-group alice project_x
perms add-to-group bob project_x

# Set project directory permissions
perms set-perms projects/x/ alice true true
perms set-perms projects/x/ bob true true
```

4. **Temporary access**
```bash
# Create temporary user
perms set-user temp_user "temp123"
perms add-to-group temp_user readers

# Set specific file permissions
perms set-perms docs/spec.pdf temp_user true false
```

5. **Revoking access**
```bash
# Remove from groups first
perms remove-from-group old_user developers
perms remove-from-group old_user project_x

# Remove specific permissions
perms set-perms src/ old_user false false
perms set-perms config/ old_user false false

# Finally delete user
perms delete-user old_user
```

### Common User Management Scenarios

1. **Initial Setup (as admin)**
```bash
# First login as admin
perms login admin admin123

# Create users with secure passwords
perms set-user alice "secure123!"
perms set-user bob "pass456@"
```

2. **Failed Non-Admin Operations**
```bash
# Login as regular user
perms login alice secure123!

# These will fail with "requires admin privileges" error
perms set-user carol pass789    # Fails - not admin
perms delete-user bob          # Fails - not admin
```

3. **User Management (as admin)**
```bash
# Login as admin first
perms login admin admin123

# Create and manage users
perms set-user temp_user temp123
perms set-user guest guest456

# Later, clean up temporary users
perms delete-user temp_user
perms delete-user guest
```

4. **Invalid Operations (even as admin)**
```bash
# These will fail even as admin
perms set-user admin newpass     # Fails - cannot modify admin
perms delete-user admin          # Fails - cannot delete admin
perms set-user alice ""          # Fails - empty password
perms delete-user unknown        # Fails - user not found
```

### Permission System Details

1. **Default Permissions**
   - New files/directories: Owner gets full permissions
   - New users: No permissions except on their own files
   - Admin: Full access to everything

2. **Group Permissions**
   - Users inherit permissions from all their groups
   - Multiple group memberships: Permissions are combined (OR)
   - Built-in groups:
     - `admins`: Full access (read/write)
     - `readers`: Read-only access
     - `writers`: Read and write access

3. **Permission Inheritance**
   - Directory permissions apply to contents
   - User-specific permissions override group permissions

4. **Special Cases**
   - User home directories: Owner has full access

### Error Handling

Common error scenarios and their meanings:

| Error Message | Possible Causes | Solution |
|--------------|-----------------|----------|
| "Permission denied" | Insufficient privileges | Login as admin or get proper permissions |
| "Not found" | File/directory doesn't exist | Check path and create if needed |
| "Already exists" | Duplicate name | Choose different name or remove existing |
| "Not empty" | Directory has contents | Remove contents first or use recursive |
| "Invalid name" | Special characters in name | Use alphanumeric names |
| "Not a directory" | Using file as directory | Check path components |
| "Not a file" | Using directory as file | Check operation target |

### Best Practices

1. **File and Directory Names**
   - Avoid spaces (use underscores)
   - Use descriptive names
   - Include extensions for files
   - Keep paths short

2. **Permissions**
   - Use groups for shared access
   - Regularly review permissions
   - Follow principle of least privilege
   - Keep track of group memberships

3. **Operations**
   - Check permissions before operations
   - Use absolute paths when unsure
   - Backup important data
   - Clean up unused files/directories

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