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

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Unix/macOS
# OR
.\venv\Scripts\activate  # On Windows
```

3. Install the package (this will also install the CLI commands):
```bash
pip install -e .
```

After installation, the `fs` and `perms` commands will be available in your virtual environment. Make sure your virtual environment is activated before using these commands.

To verify the installation:
```bash
which fs    # On Unix/macOS
where fs    # On Windows
```

## Usage

### Command Line Interface

The filesystem provides two main command-line tools:

1. `fs` - For file and directory operations
2. `perms` - For permission management

#### File System Operations (`fs`)

```bash
# Change directory
fs cd /path/to/dir

# Print working directory
fs pwd

# Create directory
fs mkdir /path/to/dir

# List directory contents
fs ls /path/to/dir

# Remove directory
fs rmdir /path/to/dir

# Create file
fs touch /path/to/file

# Write to file
fs write /path/to/file

# Read file
fs read /path/to/file

# Move file or directory
fs move /source/path /dest/path

# Find files
fs find pattern
```

#### Permission Management (`perms`)

```bash
# User Management
perms set-user username password
perms delete-user username
perms login username password

# Group Management
perms create-group groupname --read --write
perms delete-group groupname
perms add-to-group username groupname
perms remove-from-group username groupname

# Node Permissions
perms set-perms nodename username read write
perms list-perms nodename
```

## Docker Support

The project includes Docker support for easy deployment and isolation. The CLI commands (`fs` and `perms`) are automatically installed and available in the container.

### Building and Running

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

### Using Docker for Specific Commands

You can also run specific commands directly:

```bash
# Run a single fs command
docker run -it inmemory-fs fs ls /

# Run a single perms command
docker run -it inmemory-fs perms list-users

# Run with custom command
docker run -it inmemory-fs bash -c "fs mkdir /data && fs touch /data/test.txt"
```

### Data Persistence

Note that the filesystem is in-memory and container-specific. Data will be lost when the container stops. If you need to persist data between sessions:

1. Use the same container:
```bash
# Start container with a name
docker run -it --name my-fs inmemory-fs

# Later, restart and attach to the same container
docker start -ai my-fs
```

2. Or use Docker volumes (for backup/restore scenarios):
```bash
# Mount a volume for data export/import
docker run -it -v $(pwd)/fs-data:/data inmemory-fs
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run tests
python -m pytest -vv tests/
```

### Project Structure

```
inmemory_fs/
├── src/
│   ├── fs_operations/      # File system operations
│   ├── permissions/        # Permission management
│   ├── utils/             # Utility functions
│   ├── cli/               # Command line interface
│   └── models.py          # Data models
├── tests/                 # Test suite
├── requirements.txt       # Main dependencies
└── requirements-test.txt  # Test dependencies
```