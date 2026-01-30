"""
Collection traversal utilities.

This module provides utilities for traversing, reading from, and writing to
nested collections (dict, list, tuple) using dot-separated path notation.
"""

from typing import Any, Optional


def get_from_collection(container: Any, path: str) -> Optional[Any]:
    """
    Access nested items in dict/list/tuple using a dot-separated path.

    Keys are treated as strings first, then as numeric indices if the key
    is a digit. Returns None if any key/index is invalid or doesn't exist.

    Args:
        container: The collection to traverse (dict, list, or tuple).
        path: Dot-separated path string (e.g., "user.address.0.street").

    Returns:
        The value at the specified path, or None if the path is invalid.

    Raises:
        TypeError: If path is not a string.

    Examples:
        >>> data = {'user': {'name': 'Alice', 'scores': [10, 20, 30]}}
        >>> get_from_collection(data, 'user.name')
        'Alice'
        >>> get_from_collection(data, 'user.scores.1')
        20
        >>> get_from_collection(data, 'user.invalid')
        None
    """
    if not isinstance(path, str):
        raise TypeError("Path must be a string")

    if not path.strip():
        return None

    current = container
    for key in path.split('.'):
        try:
            # Try as string key
            current = current[key]
        except Exception:
            # Try digit index if the key is a digit
            if not key.isdigit():
                return None

            try:
                # Try as int index
                current = current[int(key)]
            except Exception:
                return None

    return current


def set_in_collection(container: Any, path: str, value: Any) -> bool:
    """
    Set a value in a nested collection at the specified path.

    The function traverses the collection using the dot-separated path and
    sets the value at the final key. Keys are tried as strings first, then
    as numeric indices if applicable. This function never raises exceptions
    for invalid paths or operations - it simply returns False.

    Args:
        container: The collection to modify (dict or list).
        path: Dot-separated path string where the value should be set.
        value: The value to set at the specified path.

    Returns:
        True if the operation succeeded, False otherwise.

    Raises:
        TypeError: If path is not a string.

    Examples:
        >>> data = {'user': {'name': 'Alice'}}
        >>> set_in_collection(data, 'user.name', 'Bob')
        True
        >>> data
        {'user': {'name': 'Bob'}}
        >>> set_in_collection(data, 'invalid.path', 'value')
        False
    """
    if not isinstance(path, str):
        raise TypeError("Path must be a string")

    if not path.strip():
        return False

    split_path = path.split('.')
    path_len = len(split_path)
    current = container

    # Traverse to the parent of the target location
    for i in range(path_len - 1):
        key = split_path[i]
        try:
            # Try as string key
            current = current[key]
        except Exception:
            # Try digit index if the key is a digit
            if not key.isdigit():
                return False

            try:
                # Try as int index
                current = current[int(key)]
            except Exception:
                return False

    # Set the value at the final key
    last_key = split_path[-1]
    try:
        # Try as string key first
        current[last_key] = value
        return True
    except Exception:
        # Fallback to int index if the key is a digit
        if last_key.isdigit():
            try:
                current[int(last_key)] = value
                return True
            except Exception:
                return False
        return False