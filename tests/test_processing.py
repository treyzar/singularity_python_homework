from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


def test_filter_by_state_default(operations: list[dict[str, Any]]) -> None:
    assert [op["id"] for op in filter_by_state(operations)] == [1, 3]


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2, 5]),
        ("PENDING", [4]),
        ("UNKNOWN", []),
        ("executed", []),
        ("", []),
    ],
)
def test_filter_by_state(operations: list[dict[str, Any]], state: str, expected_ids: list[int]) -> None:
    assert [op["id"] for op in filter_by_state(operations, state)] == expected_ids


def test_filter_by_state_empty_list() -> None:
    assert filter_by_state([]) == []


def test_filter_by_state_skips_operations_without_state() -> None:
    assert filter_by_state([{"id": 1}, {"id": 2, "state": "EXECUTED"}]) == [{"id": 2, "state": "EXECUTED"}]


def test_filter_by_state_does_not_modify_input(operations: list[dict[str, Any]]) -> None:
    original = list(operations)
    result = filter_by_state(operations)
    assert operations == original
    assert result is not operations


@pytest.mark.parametrize(
    "reverse, expected_ids",
    [
        (True, [1, 4, 5, 3, 2]),
        (False, [2, 3, 4, 5, 1]),
    ],
)
def test_sort_by_date_order(operations: list[dict[str, Any]], reverse: bool, expected_ids: list[int]) -> None:
    assert [op["id"] for op in sort_by_date(operations, reverse=reverse)] == expected_ids


def test_sort_by_date_default_is_descending(operations: list[dict[str, Any]]) -> None:
    assert sort_by_date(operations) == sort_by_date(operations, reverse=True)


@pytest.mark.parametrize("reverse", [True, False])
def test_sort_by_date_equal_dates(operations_with_equal_dates: list[dict[str, Any]], reverse: bool) -> None:
    result = sort_by_date(operations_with_equal_dates, reverse=reverse)
    equal_ids = sorted(op["id"] for op in result if op["date"] == "2024-03-11T02:26:18")
    assert equal_ids == [1, 2]
    assert len(result) == 3


def test_sort_by_date_empty_list() -> None:
    assert sort_by_date([]) == []


def test_sort_by_date_does_not_modify_input(operations: list[dict[str, Any]]) -> None:
    original = list(operations)
    sort_by_date(operations)
    assert operations == original


@pytest.mark.parametrize("bad_date", ["не дата", "03.07.2019", "", "2019-13-45"])
def test_sort_by_date_invalid_date_format(bad_date: str) -> None:
    with pytest.raises(ValueError):
        sort_by_date([{"date": "2019-07-03T18:35:29"}, {"date": bad_date}])


def test_sort_by_date_missing_date() -> None:
    with pytest.raises(KeyError):
        sort_by_date([{"id": 1}, {"id": 2, "date": "2019-07-03T18:35:29"}])
