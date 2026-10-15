from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.readers import read_transactions_from_csv, read_transactions_from_excel

ROWS = [
    {
        "id": "650703",
        "state": "EXECUTED",
        "date": "2023-09-05T11:30:32Z",
        "amount": "16210",
        "currency_name": "Sol",
        "currency_code": "PEN",
        "from": "Счет 58803664561298323391",
        "to": "Счет 39745660563456619397",
        "description": "Перевод организации",
    },
    {
        "id": "3598919",
        "state": "EXECUTED",
        "date": "2020-12-06T23:00:58Z",
        "amount": "29740",
        "currency_name": "Peso",
        "currency_code": "COP",
        "from": "",
        "to": "Счет 23294994494356835683",
        "description": "Открытие вклада",
    },
]

EXPECTED = [
    {
        "id": 650703,
        "state": "EXECUTED",
        "date": "2023-09-05T11:30:32Z",
        "operationAmount": {"amount": "16210", "currency": {"name": "Sol", "code": "PEN"}},
        "description": "Перевод организации",
        "from": "Счет 58803664561298323391",
        "to": "Счет 39745660563456619397",
    },
    {
        "id": 3598919,
        "state": "EXECUTED",
        "date": "2020-12-06T23:00:58Z",
        "operationAmount": {"amount": "29740", "currency": {"name": "Peso", "code": "COP"}},
        "description": "Открытие вклада",
        "to": "Счет 23294994494356835683",
    },
]


@patch("src.readers.pd.read_csv")
def test_read_transactions_from_csv(mock_read_csv: Mock) -> None:
    mock_read_csv.return_value = pd.DataFrame(ROWS)

    assert read_transactions_from_csv("transactions.csv") == EXPECTED
    mock_read_csv.assert_called_once_with("transactions.csv", sep=";", dtype=str, keep_default_na=False)


@patch("src.readers.pd.read_csv")
def test_read_transactions_from_csv_skips_empty_rows(mock_read_csv: Mock) -> None:
    mock_read_csv.return_value = pd.DataFrame([ROWS[0], {key: "" for key in ROWS[0]}])

    assert read_transactions_from_csv("transactions.csv") == EXPECTED[:1]


@pytest.mark.parametrize("error", [FileNotFoundError, pd.errors.EmptyDataError])
def test_read_transactions_from_csv_returns_empty_list_on_error(error: type[Exception]) -> None:
    with patch("src.readers.pd.read_csv", Mock(side_effect=error)) as mock_read_csv:
        assert read_transactions_from_csv("transactions.csv") == []
    mock_read_csv.assert_called_once()


def test_read_transactions_from_csv_real_file(tmp_path: Path) -> None:
    path = tmp_path / "transactions.csv"
    pd.DataFrame(ROWS).to_csv(path, sep=";", index=False)

    assert read_transactions_from_csv(str(path)) == EXPECTED


@patch("src.readers.pd.read_excel")
def test_read_transactions_from_excel(mock_read_excel: Mock) -> None:
    mock_read_excel.return_value = pd.DataFrame(ROWS)

    assert read_transactions_from_excel("transactions_excel.xlsx") == EXPECTED
    mock_read_excel.assert_called_once_with("transactions_excel.xlsx", dtype=str, keep_default_na=False)


@patch("src.readers.pd.read_excel")
def test_read_transactions_from_excel_empty_sheet(mock_read_excel: Mock) -> None:
    mock_read_excel.return_value = pd.DataFrame()

    assert read_transactions_from_excel("transactions_excel.xlsx") == []


def test_read_transactions_from_excel_file_not_found() -> None:
    with patch("src.readers.pd.read_excel", Mock(side_effect=FileNotFoundError)) as mock_read_excel:
        assert read_transactions_from_excel("missing.xlsx") == []
    mock_read_excel.assert_called_once_with("missing.xlsx", dtype=str, keep_default_na=False)


def test_read_transactions_from_excel_real_file(tmp_path: Path) -> None:
    path = tmp_path / "transactions_excel.xlsx"
    pd.DataFrame(ROWS).to_excel(path, index=False)

    assert read_transactions_from_excel(str(path)) == EXPECTED
