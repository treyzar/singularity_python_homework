from unittest.mock import mock_open, patch

import pytest

from src.utils import get_transactions


def test_get_transactions_returns_list() -> None:
    file_data = '[{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}]'
    with patch("builtins.open", mock_open(read_data=file_data)) as mocked_open:
        result = get_transactions("data/operations.json")

    assert result == [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}]
    mocked_open.assert_called_once_with("data/operations.json", encoding="utf-8")


@pytest.mark.parametrize("file_data", ["", "not json", '{"id": 1}', "42"])
def test_get_transactions_returns_empty_list_for_bad_content(file_data: str) -> None:
    with patch("builtins.open", mock_open(read_data=file_data)):
        assert get_transactions("data/operations.json") == []


def test_get_transactions_returns_empty_list_when_file_not_found() -> None:
    with patch("builtins.open", side_effect=FileNotFoundError):
        assert get_transactions("missing.json") == []
