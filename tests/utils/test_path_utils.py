import pytest
from src.utils.path_utils import split_path, join_path, normalize_path, get_parent_path, get_basename

def test_split_path():
    assert split_path("") == []
    assert split_path("/") == ["/"]
    assert split_path("/usr/local/bin") == ["/", "usr", "local", "bin"]
    assert split_path("usr/local/bin") == ["usr", "local", "bin"]
    assert split_path("/usr//local/bin") == ["/", "usr", "local", "bin"]
    assert split_path("./usr/local") == [".", "usr", "local"]

def test_join_path():
    assert join_path([]) == ""
    assert join_path(["/", "usr", "local", "bin"]) == "/usr/local/bin"
    assert join_path(["usr", "local", "bin"]) == "usr/local/bin"
    assert join_path(["/", "usr", "local", "bin"]) == "/usr/local/bin"
    assert join_path(["/", "usr", "", "local", "bin"]) == "/usr/local/bin"

def test_normalize_path():
    assert normalize_path("") == ""
    assert normalize_path("/") == "/"
    assert normalize_path("/usr/local/bin") == "/usr/local/bin"
    assert normalize_path("/usr/local/../bin") == "/usr/bin"
    assert normalize_path("/usr/./local/bin") == "/usr/local/bin"
    assert normalize_path("/usr/local/bin/..") == "/usr/local"
    assert normalize_path("./usr/local") == "usr/local"
    assert normalize_path("/usr/../../local") == "/local"
    assert normalize_path("/usr/../../../local") == "/local"

def test_get_parent_path():
    assert get_parent_path("") == "/"
    assert get_parent_path("/") == "/"
    assert get_parent_path(".") == "/"
    assert get_parent_path("/usr/local/bin") == "/usr/local"
    assert get_parent_path("/usr") == "/"
    assert get_parent_path("usr/local") == "usr"
    assert get_parent_path("usr") == "/"

def test_get_basename():
    assert get_basename("") == ""
    assert get_basename("/") == ""
    assert get_basename("/usr/local/bin") == "bin"
    assert get_basename("/usr") == "usr"
    assert get_basename("usr/local") == "local"
    assert get_basename("file.txt") == "file.txt" 