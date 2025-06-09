# In-Memory Filesystem with Permissions

This project is a modular, thread-safe, in-memory filesystem written in Python. It supports:
- File and directory operations (mkdir, ls, cd, read, write, etc.)
- Per-user permission management (read/write)
- Admin-only user management and permission grants

## 🚀 Getting Started

### [Recommended] Docker

You can run the file system in a Docker container. This ensures consistent behavior across different environments.

#### Building the Docker Image

```bash
# Build the image
docker build -t inmemory-fs .
```

#### Running the Container

```bash
# Run the container in interactive mode
docker run -it inmemory-fs

# Now you can use the file system commands inside the container:
fs pwd
perms set-user swathi pass123
```

#### Running Specific Commands

You can also run specific commands directly:

```bash
# Run a filesystem command
docker run -it inmemory-fs fs ls

# Run a permissions command
docker run -it inmemory-fs perms list-perms document.txt
```

Note: The commands `fs` and `perms` are shortcuts for `./filesys.py` and `./permissions.py` respectively.

#### Development with Docker

For development, you can mount your local directory:

```bash
docker run -it -v $(pwd):/app inmemory-fs
```

This will allow you to edit files locally while running them in the container.

### Local setup

- Python 3.9+

### Initial Setup

The system comes with a default admin user:
- Username: `admin`
- Password: `admin123`

The admin user has special privileges:
- Create and manage users
- Set permissions for files and directories
- Full access to all operations
- Cannot be modified or deleted

## Command-Line Tools

The system provides two command-line tools:
1. `filesys.py` - For file and directory operations
2. `permissions.py` - For user and permission management

Make both scripts executable:
```bash
chmod +x filesys.py
chmod +x permissions.py
```

## 🔐 Permission Management

The file system includes a robust permission management system with user authentication and group-based access control.

### User Management

```bash
# Create a new user (admin only)
./permissions.py set-user swathi pass123

# Delete a user (admin only)
./permissions.py delete-user swathi

# Login as a user
./permissions.py login swathi pass123
```

### Permission Groups

The system supports permission groups for easier access management:

```bash
# Create a new group (admin only)
./permissions.py create-group developers --read --write
./permissions.py create-group viewers --read

# Add users to groups (admin only)
./permissions.py add-to-group swathi developers
./permissions.py add-to-group bala viewers

# Remove users from groups (admin only)
./permissions.py remove-from-group bala viewers

# Delete a group (admin only)
./permissions.py delete-group viewers

# List all groups and their members
./permissions.py list-groups
```

Default Groups:
- `readers`: Read-only access
- `writers`: Read and write access
- `admins`: Full access (includes admin user)

### Node Permissions

```bash
# Set direct permissions for a node (admin only)
./permissions.py set-perms document.txt swathi true false  # read-only
./permissions.py set-perms document.txt bala true true  # read-write

# List permissions for a node
./permissions.py list-perms document.txt
```

The output will show both direct permissions and permissions inherited from groups:
```
Permissions for document.txt:

User: swathi
  direct: read=true, write=false
  via developers: read=true, write=true

User: bala
  direct: read=true, write=true
```

### Permission Inheritance

1. Admin user always has full access
2. Node owner has full access to their nodes
3. Direct permissions take precedence over group permissions
4. A user can have permissions from multiple groups
5. Read/write access can be granted independently

## File System Commands (filesys.py)

File system commands are available to all users, but access is controlled by permissions.

### Directory Operations

1. Change Directory (cd)
```bash
# Change to a subdirectory
./filesys.py cd documents

# Change to parent directory
./filesys.py cd ..

# Change to absolute path
./filesys.py cd /home/documents
```

2. Print Working Directory (pwd)
```bash
# Show current directory path
./filesys.py pwd
# Example output: /home/documents
```

3. List Directory Contents (ls)
```bash
# List all files and directories in current directory
./filesys.py ls
# Example output: ['documents', 'photos', 'notes.txt']
```

4. Create Directory (mkdir)
```bash
# Create a new directory
./filesys.py mkdir projects
```

5. Remove Directory (rmdir)
```bash
# Remove an empty directory
./filesys.py rmdir old_projects
```

### File Operations

1. Create File (touch)
```bash
# Create a new empty file
./filesys.py touch notes.txt
```

2. Write to File (write)
```bash
# Write content to a file
./filesys.py write notes.txt "This is my note"
```

3. Read File (read)
```bash
# Display file contents
./filesys.py read notes.txt
```

4. Move/Rename File (move)
```bash
# Rename a file
./filesys.py move old_name.txt new_name.txt
```

### Search Operations

1. Find Files/Directories (find)
```bash
# Find all files/directories named "notes.txt"
./filesys.py find notes.txt
# Example output:
# Found notes.txt at:
#   /documents/notes.txt
#   /backup/notes.txt
```

## Error Handling

The system provides clear error messages for various scenarios:

### Permission Errors
- "Only admin can create new users"
- "Only admin can set permissions"
- "Read permission denied"
- "Write permission denied"
- "Cannot modify admin user"

### Authentication Errors
- "User not found"
- "Invalid password"
- "Password is required"

### File/Directory Errors
- File/directory already exists
- File/directory not found
- Invalid path
- Insufficient permissions
- Directory not empty (when trying to remove)

## Examples of Common Workflows

### User and Permission Setup

1. Initial Admin Setup:
```bash
# Login as admin
./permissions.py login admin admin123

# Create team members
./permissions.py set-user swathi pass123
./permissions.py set-user bala pass456
./permissions.py set-user bhat pass789
```

2. Configure Project Access:
```bash
# As admin, set up project structure
./filesys.py mkdir projects
./filesys.py cd projects
./filesys.py touch plan.txt
./filesys.py write plan.txt "Project Timeline"

# Grant permissions to team
./permissions.py set-perms plan.txt swathi true true   # full access
./permissions.py set-perms plan.txt bala true false    # read-only
./permissions.py set-perms plan.txt bhat true false  # read-only
```

3. User Workflow:
```bash
# Login as regular user
./permissions.py login alice pass123

# Work with allowed files
./filesys.py cd projects
./filesys.py read plan.txt
./filesys.py write plan.txt "Updated Project Timeline"  # Works for swathi
```

4. Permission Verification:
```bash
# Login as admin to check permissions
./permissions.py login admin admin123
./permissions.py list-perms plan.txt

# Try as restricted user
./permissions.py login bala pass456
./filesys.py read plan.txt        # Works (has read permission)
./filesys.py write plan.txt "X"   # Fails (no write permission)
```