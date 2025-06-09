"""Utility functions for path manipulation"""

def split_path(path: str) -> list:
    """Split a path into its components"""
    if not path:
        return []
    if path == "/":
        return ["/"]
    parts = path.split("/")
    if path.startswith("/"):
        parts[0] = "/"
    return [p for p in parts if p]

def join_path(parts: list) -> str:
    """Join path components into a single path"""
    if not parts:
        return ""
    # Filter out empty parts
    filtered_parts = [p for p in parts if p]
    if not filtered_parts:
        return ""
    if filtered_parts[0] == "/":
        return "/" + "/".join(filtered_parts[1:])
    return "/".join(filtered_parts)

def normalize_path(path: str) -> str:
    """Normalize a path by removing . and .. components"""
    if not path:
        return ""
    if path == "/":
        return "/"

    parts = split_path(path)
    result = []

    for part in parts:
        if part == ".":
            continue
        elif part == "..":
            if result and result[-1] != "/":
                result.pop()
        else:
            result.append(part)

    return join_path(result)

def get_parent_path(path: str) -> str:
    """Get the parent path of a given path"""
    if not path or path == "/" or path == ".":
        return "/"

    parts = split_path(path)
    if len(parts) <= 1:
        return "/"

    return join_path(parts[:-1])

def get_basename(path: str) -> str:
    """Get the basename (final component) of a path"""
    if not path or path == "/":
        return ""

    parts = split_path(path)
    return parts[-1] if parts else "" 