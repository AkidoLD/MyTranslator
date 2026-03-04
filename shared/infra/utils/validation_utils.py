from types import UnionType
from typing import Any


def validate_type(value, expected_type: type, name: str):
    if not isinstance(value, expected_type):
        raise TypeError(f"{name} must be {expected_type.__name__}, got {type(value).__name__}")
    return value

def validate_type_or_none(value, expected_type: type, name: str):
    if value is None : return None
    return validate_type(value, expected_type, name)

def validate_not_empty(value: Any, name: str) -> str:
    if not value:
        raise ValueError(f"{name} cannot be empty.")
    return value

def validate_callable(value, name: str):
    if value is not None and not callable(value):
        raise TypeError(f"{name} must be callable or None, got {type(value).__name__}")
    return value