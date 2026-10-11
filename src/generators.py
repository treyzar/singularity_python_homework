from typing import Any, Iterator

CARD_NUMBER_MIN = 1
CARD_NUMBER_MAX = 9999_9999_9999_9999


def filter_by_currency(transactions: list[dict[str, Any]], currency: str) -> Iterator[dict[str, Any]]:
    """Return an iterator over transactions made in the given currency.

    The currency is compared with ``operationAmount.currency.code``. Transactions
    without this data are skipped.
    """
    return (
        transaction
        for transaction in transactions
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency
    )


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Iterator[str]:
    """Yield the description of each transaction one by one.

    A transaction without a ``description`` key yields an empty string.
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Yield card numbers in the ``XXXX XXXX XXXX XXXX`` format from ``start`` to ``stop`` inclusive.

    Both bounds must be in the range from 1 to 9999999999999999 and ``start`` must
    not be greater than ``stop``, otherwise ``ValueError`` is raised on the first request.
    """
    if not (CARD_NUMBER_MIN <= start <= CARD_NUMBER_MAX and CARD_NUMBER_MIN <= stop <= CARD_NUMBER_MAX):
        raise ValueError("Границы диапазона должны быть от 1 до 9999999999999999")
    if start > stop:
        raise ValueError("Начало диапазона не может быть больше конца")

    for number in range(start, stop + 1):
        digits = f"{number:016d}"
        yield " ".join(digits[index : index + 4] for index in range(0, 16, 4))


if __name__ == "__main__":
    for card_number in card_number_generator(1, 3):
        print(card_number)
