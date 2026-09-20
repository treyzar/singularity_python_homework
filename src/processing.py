from typing import Any


def filter_by_state(
    operations: list[dict[str, Any]], state: str = "EXECUTED"
) -> list[dict[str, Any]]:
    """Return operations whose state matches the requested value.

    The input list is not modified. Operations without a ``state`` key are
    excluded.
    """
    return [operation for operation in operations if operation.get("state") == state]
