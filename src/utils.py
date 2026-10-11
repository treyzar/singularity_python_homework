import json
from typing import Any


def get_transactions(path: str) -> list[dict[str, Any]]:
    """Return a list of financial transactions loaded from a JSON file.

    An empty list is returned if the file is not found, is empty, contains
    invalid JSON or its top-level value is not a list.
    """
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []
    return data
