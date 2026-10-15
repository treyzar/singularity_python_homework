from typing import Any

import pandas as pd


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    """Convert a flat CSV/XLSX row to the transaction format used in the JSON file.

    Columns ``amount``, ``currency_name`` and ``currency_code`` are moved to the
    nested ``operationAmount`` dictionary. Empty ``from`` and ``to`` fields are
    dropped.
    """
    transaction: dict[str, Any] = {
        "id": int(row["id"]) if str(row.get("id", "")).isdigit() else row.get("id"),
        "state": row.get("state", ""),
        "date": row.get("date", ""),
        "operationAmount": {
            "amount": row.get("amount", ""),
            "currency": {"name": row.get("currency_name", ""), "code": row.get("currency_code", "")},
        },
        "description": row.get("description", ""),
    }
    for field in ("from", "to"):
        if row.get(field):
            transaction[field] = row[field]
    return transaction


def _to_transactions(data_frame: pd.DataFrame) -> list[dict[str, Any]]:
    """Return a list of transactions built from the rows of a data frame.

    Rows in which all cells are empty are skipped.
    """
    records = data_frame.fillna("").astype(str).to_dict(orient="records")
    return [
        _normalize_row({str(key): value for key, value in record.items()})
        for record in records
        if any(value.strip() for value in record.values())
    ]


def read_transactions_from_csv(path: str) -> list[dict[str, Any]]:
    """Return a list of transactions read from a CSV file with ``;`` as a separator.

    An empty list is returned if the file is not found or is empty.
    """
    try:
        data_frame = pd.read_csv(path, sep=";", dtype=str, keep_default_na=False)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return []
    return _to_transactions(data_frame)


def read_transactions_from_excel(path: str) -> list[dict[str, Any]]:
    """Return a list of transactions read from the first sheet of an XLSX file.

    An empty list is returned if the file is not found.
    """
    try:
        data_frame = pd.read_excel(path, dtype=str, keep_default_na=False)
    except FileNotFoundError:
        return []
    return _to_transactions(data_frame)
