from typing import Any

import pytest


@pytest.fixture
def operations() -> list[dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "CANCELED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 3, "state": "EXECUTED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 4, "state": "PENDING", "date": "2018-10-14T08:21:33.419441"},
        {"id": 5, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def operations_with_equal_dates() -> list[dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18"},
        {"id": 2, "state": "EXECUTED", "date": "2024-03-11T02:26:18"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-01T00:00:00"},
    ]


@pytest.fixture
def valid_card_number() -> str:
    return "7000792289606361"


@pytest.fixture
def valid_account_number() -> str:
    return "73654108430135874305"
