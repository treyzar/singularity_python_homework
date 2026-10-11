import logging

import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number(valid_card_number: str) -> None:
    assert get_mask_card_number(valid_card_number) == "7000 79** **** 6361"


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567812345678", "1234 56** **** 5678"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("  7000792289606361  ", "7000 79** **** 6361"),
    ],
)
def test_get_mask_card_number_formats(card_number: str, expected: str) -> None:
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "card_number",
    ["", "   ", "123", "123456781234567", "12345678123456789", "1234 5678 1234 5678", "70007922896063ab"],
)
def test_get_mask_card_number_invalid(card_number: str) -> None:
    with pytest.raises(ValueError, match="16 цифр"):
        get_mask_card_number(card_number)


def test_get_mask_account(valid_account_number: str) -> None:
    assert get_mask_account(valid_account_number) == "**4305"


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("1234", "**1234"),
        ("12345", "**2345"),
        ("73654108430135874305", "**4305"),
        (" 98765432 ", "**5432"),
    ],
)
def test_get_mask_account_lengths(account_number: str, expected: str) -> None:
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize("account_number", ["", "   ", "1", "123", "12ab56", "-12345"])
def test_get_mask_account_invalid(account_number: str) -> None:
    with pytest.raises(ValueError, match="минимум 4 цифры"):
        get_mask_account(account_number)


def test_masks_log_success(caplog: pytest.LogCaptureFixture, valid_card_number: str) -> None:
    with caplog.at_level(logging.DEBUG, logger="masks"):
        get_mask_card_number(valid_card_number)
        get_mask_account("73654108430135874305")

    assert ("masks", logging.INFO, "Номер карты замаскирован: 7000 79** **** 6361") in caplog.record_tuples
    assert ("masks", logging.INFO, "Номер счета замаскирован: **4305") in caplog.record_tuples


def test_masks_log_errors(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(ValueError):
        get_mask_card_number("123")
    with pytest.raises(ValueError):
        get_mask_account("12")

    error_records = [record for record in caplog.records if record.name == "masks" and record.levelno == logging.ERROR]
    assert len(error_records) == 2
