from pathlib import Path
from typing import Any, Callable

from src.generators import filter_by_currency
from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.readers import read_transactions_from_csv, read_transactions_from_excel
from src.utils import get_transactions
from src.widget import get_date, mask_account_card

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

FILE_SOURCES: dict[str, tuple[str, Callable[[str], list[dict[str, Any]]], Path]] = {
    "1": ("JSON", get_transactions, DATA_DIR / "operations.json"),
    "2": ("CSV", read_transactions_from_csv, DATA_DIR / "transactions.csv"),
    "3": ("XLSX", read_transactions_from_excel, DATA_DIR / "transactions_excel.xlsx"),
}
STATES = ("EXECUTED", "CANCELED", "PENDING")
YES_ANSWERS = ("да", "yes", "y", "д")
NO_ANSWERS = ("нет", "no", "n", "н")
ASCENDING_ANSWERS = ("по возрастанию", "возрастанию", "возрастание")
DESCENDING_ANSWERS = ("по убыванию", "убыванию", "убывание")


def choose_file() -> list[dict[str, Any]]:
    """Ask the user to choose a file type and return transactions read from that file."""
    print(
        "Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )
    while True:
        choice = input().strip()
        if choice in FILE_SOURCES:
            file_type, reader, path = FILE_SOURCES[choice]
            print(f"Для обработки выбран {file_type}-файл.")
            return reader(str(path))
        print("Пункт меню недоступен. Введите 1, 2 или 3.")


def choose_state() -> str:
    """Ask the user for an operation state until a valid one is entered and return it in upper case."""
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            f"Доступные для фильтровки статусы: {', '.join(STATES)}"
        )
        state = input().strip()
        if state.upper() in STATES:
            print(f'Операции отфильтрованы по статусу "{state.upper()}"')
            return state.upper()
        print(f'Статус операции "{state}" недоступен.')


def ask_yes_no(question: str) -> bool:
    """Ask a yes/no question until a valid answer is entered and return ``True`` for "yes"."""
    while True:
        print(question)
        answer = input().strip().lower()
        if answer in YES_ANSWERS:
            return True
        if answer in NO_ANSWERS:
            return False
        print("Ответьте, пожалуйста, Да или Нет.")


def ask_sort_reverse() -> bool:
    """Ask the sort order until a valid answer is entered and return ``True`` for descending order."""
    while True:
        print("Отсортировать по возрастанию или по убыванию?")
        answer = input().strip().lower()
        if answer in ASCENDING_ANSWERS:
            return False
        if answer in DESCENDING_ANSWERS:
            return True
        print("Ответьте, пожалуйста, по возрастанию или по убыванию.")


def format_transaction(transaction: dict[str, Any]) -> str:
    """Return a transaction as text: date and description, masked accounts and amount."""
    amount = transaction.get("operationAmount", {})
    currency = amount.get("currency", {})
    currency_name = "руб." if currency.get("code") == "RUB" else currency.get("code", "")
    route = " -> ".join(mask_account_card(transaction[field]) for field in ("from", "to") if transaction.get(field))
    lines = [f"{get_date(transaction['date'])} {transaction.get('description', '')}"]
    if route:
        lines.append(route)
    lines.append(f"Сумма: {amount.get('amount', '')} {currency_name}")
    return "\n".join(lines)


def filter_transactions(transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Ask the user for filter and sort options and return the matching transactions."""
    result = filter_by_state(transactions, choose_state())
    if ask_yes_no("Отсортировать операции по дате? Да/Нет"):
        result = sort_by_date(result, reverse=ask_sort_reverse())
    if ask_yes_no("Выводить только рублевые транзакции? Да/Нет"):
        result = list(filter_by_currency(result, "RUB"))
    if ask_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет"):
        print("Введите слово для поиска:")
        result = process_bank_search(result, input().strip())
    return result


def main() -> None:
    """Run the interactive program: read transactions, filter them by user choices and print the result."""
    transactions = choose_file()
    result = filter_transactions(transactions)
    print("Распечатываю итоговый список транзакций...")
    if not result:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return
    print(f"Всего банковских операций в выборке: {len(result)}\n")
    print("\n\n".join(format_transaction(transaction) for transaction in result))


if __name__ == "__main__":
    main()
