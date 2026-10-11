import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "info, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("счет 35383033474447895560", "счет **5560"),
    ],
)
def test_mask_account_card(info: str, expected: str) -> None:
    assert mask_account_card(info) == expected


def test_mask_account_card_uses_fixtures(valid_card_number: str, valid_account_number: str) -> None:
    assert mask_account_card(f"Visa {valid_card_number}") == "Visa 7000 79** **** 6361"
    assert mask_account_card(f"Счет {valid_account_number}") == "Счет **4305"


@pytest.mark.parametrize("info", ["", "   "])
def test_mask_account_card_empty(info: str) -> None:
    with pytest.raises(ValueError, match="Не передана информация"):
        mask_account_card(info)


@pytest.mark.parametrize("info", ["7000792289606361", "Visa"])
def test_mask_account_card_without_type_or_number(info: str) -> None:
    with pytest.raises(ValueError, match="тип и номер"):
        mask_account_card(info)


@pytest.mark.parametrize("info", ["Visa 123", "Visa abcdefghijklmnop", "Счет 12", "Счет abcd"])
def test_mask_account_card_invalid_number(info: str) -> None:
    with pytest.raises(ValueError):
        mask_account_card(info)


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-03-11T02:26:18", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),
        ("2000-01-01T00:00:00", "01.01.2000"),
        ("2024-12-31T23:59:59.999999", "31.12.2024"),
        ("2024-02-29T12:00:00", "29.02.2024"),
    ],
)
def test_get_date(date_string: str, expected: str) -> None:
    assert get_date(date_string) == expected


@pytest.mark.parametrize(
    "date_string",
    ["", "не дата", "11.03.2024", "2024-13-01T00:00:00", "2023-02-29T00:00:00"],
)
def test_get_date_invalid(date_string: str) -> None:
    with pytest.raises(ValueError):
        get_date(date_string)
