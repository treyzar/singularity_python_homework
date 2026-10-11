from typing import Any, Iterator

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_returns_iterator(transactions: list[dict[str, Any]]) -> None:
    result = filter_by_currency(transactions, "USD")
    assert isinstance(result, Iterator)
    assert next(result)["id"] == 939719570


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("USD", [939719570, 142264268, 895315941]),
        ("RUB", [873106923, 594226727]),
        ("EUR", []),
        ("usd", []),
        ("", []),
    ],
)
def test_filter_by_currency(transactions: list[dict[str, Any]], currency: str, expected_ids: list[int]) -> None:
    assert [item["id"] for item in filter_by_currency(transactions, currency)] == expected_ids


def test_filter_by_currency_empty_list() -> None:
    assert list(filter_by_currency([], "USD")) == []


def test_filter_by_currency_skips_transactions_without_currency() -> None:
    broken: list[dict[str, Any]] = [
        {"id": 1},
        {"id": 2, "operationAmount": {}},
        {"id": 3, "operationAmount": {"currency": {}}},
    ]
    assert list(filter_by_currency(broken, "USD")) == []


def test_filter_by_currency_is_exhausted(transactions: list[dict[str, Any]]) -> None:
    result = filter_by_currency(transactions, "RUB")
    next(result)
    next(result)
    with pytest.raises(StopIteration):
        next(result)


def test_transaction_descriptions(transactions: list[dict[str, Any]]) -> None:
    descriptions = transaction_descriptions(transactions)
    assert isinstance(descriptions, Iterator)
    assert [next(descriptions) for _ in range(5)] == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]


@pytest.mark.parametrize("count", [0, 1, 3, 5])
def test_transaction_descriptions_count(transactions: list[dict[str, Any]], count: int) -> None:
    assert len(list(transaction_descriptions(transactions[:count]))) == count


def test_transaction_descriptions_empty_list() -> None:
    assert list(transaction_descriptions([])) == []


def test_transaction_descriptions_without_description() -> None:
    assert list(transaction_descriptions([{"id": 1}])) == [""]


def test_card_number_generator() -> None:
    assert list(card_number_generator(1, 5)) == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 1, ["0000 0000 0000 0001"]),
        (9999, 10001, ["0000 0000 0000 9999", "0000 0000 0001 0000", "0000 0000 0001 0001"]),
        (1234567812345678, 1234567812345678, ["1234 5678 1234 5678"]),
        (9999999999999998, 9999999999999999, ["9999 9999 9999 9998", "9999 9999 9999 9999"]),
    ],
)
def test_card_number_generator_ranges(start: int, stop: int, expected: list[str]) -> None:
    assert list(card_number_generator(start, stop)) == expected


def test_card_number_generator_is_lazy_and_finishes() -> None:
    generator = card_number_generator(1, 2)
    assert isinstance(generator, Iterator)
    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"
    with pytest.raises(StopIteration):
        next(generator)


@pytest.mark.parametrize(
    "start, stop", [(0, 5), (-1, 5), (1, 0), (1, 10000000000000000), (10000000000000000, 10000000000000001)]
)
def test_card_number_generator_out_of_range(start: int, stop: int) -> None:
    with pytest.raises(ValueError, match="от 1 до 9999999999999999"):
        next(card_number_generator(start, stop))


def test_card_number_generator_start_greater_than_stop() -> None:
    with pytest.raises(ValueError, match="не может быть больше"):
        next(card_number_generator(5, 1))
