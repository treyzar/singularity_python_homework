from datetime import datetime
from typing import Any


def filter_by_state(
    operations: list[dict[str, Any]], state: str = "EXECUTED"
) -> list[dict[str, Any]]:
    """Return operations whose state matches the requested value.

    The input list is not modified. Operations without a ``state`` key are
    excluded.
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(
    operations: list[dict[str, Any]], reverse: bool = True
) -> list[dict[str, Any]]:
    """Return a new list of operations sorted by their ISO 8601 date.

    By default, the most recent operation comes first. The input list is not
    modified.
    """
    return sorted(
        operations,
        key=lambda operation: datetime.fromisoformat(operation["date"]),
        reverse=reverse,
    )
