import re
from collections import Counter
from datetime import datetime
from typing import Any


def filter_by_state(operations: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """Return operations whose state matches the requested value.

    The input list is not modified. Operations without a ``state`` key are
    excluded.
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operations: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Return a new list of operations sorted by their ISO 8601 date.

    By default, the most recent operation comes first. The input list is not
    modified.
    """
    return sorted(
        operations,
        key=lambda operation: datetime.fromisoformat(operation["date"]),
        reverse=reverse,
    )


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """Return operations whose description contains the search string.

    The search is case-insensitive and is done with a regular expression, special
    characters of the search string are matched literally. Operations without a
    ``description`` key are excluded.
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [operation for operation in data if pattern.search(operation.get("description", ""))]


def process_bank_operations(data: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """Return the number of operations in each of the given categories.

    The category of an operation is its ``description``. Every requested category
    is present in the result, categories without operations have the value 0.
    """
    counter = Counter(operation.get("description") for operation in data if operation.get("description") in categories)
    return {category: counter[category] for category in categories}
