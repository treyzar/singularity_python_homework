from typing import Any
from unittest.mock import Mock, patch

import pytest

from src.main import ask_sort_reverse, ask_yes_no, choose_file, choose_state, format_transaction, main


def run_with_input(answers: list[str], func: Any) -> Any:
    """Call ``func`` with ``input`` returning the given answers one by one."""
    with patch("builtins.input", side_effect=answers):
        return func()


@pytest.mark.parametrize("choice, file_type", [("1", "JSON"), ("2", "CSV"), ("3", "XLSX")])
def test_choose_file(capsys: pytest.CaptureFixture[str], choice: str, file_type: str) -> None:
    reader = Mock(return_value=[{"id": 1}])
    with patch.dict("src.main.FILE_SOURCES", {choice: (file_type, reader, "file")}):
        assert run_with_input(["4", choice], choose_file) == [{"id": 1}]

    output = capsys.readouterr().out
    assert "Привет! Добро пожаловать" in output
    assert "Пункт меню недоступен" in output
    assert f"Для обработки выбран {file_type}-файл." in output
    reader.assert_called_once_with("file")


@pytest.mark.parametrize(
    "choice, reader_name",
    [("1", "get_transactions"), ("2", "read_transactions_from_csv"), ("3", "read_transactions_from_excel")],
)
def test_file_sources_readers(choice: str, reader_name: str) -> None:
    import src.main as main_module

    assert main_module.FILE_SOURCES[choice][1] is getattr(main_module, reader_name)


@pytest.mark.parametrize("answer", ["EXECUTED", "executed", "Executed", " executed "])
def test_choose_state_ignores_case(capsys: pytest.CaptureFixture[str], answer: str) -> None:
    assert run_with_input([answer], choose_state) == "EXECUTED"
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in capsys.readouterr().out


def test_choose_state_repeats_on_wrong_status(capsys: pytest.CaptureFixture[str]) -> None:
    assert run_with_input(["test", "pending"], choose_state) == "PENDING"
    output = capsys.readouterr().out
    assert 'Статус операции "test" недоступен.' in output
    assert output.count("Введите статус") == 2


@pytest.mark.parametrize("answers, expected", [(["Да"], True), (["нет"], False), (["может", "ДА"], True)])
def test_ask_yes_no(answers: list[str], expected: bool) -> None:
    assert run_with_input(answers, lambda: ask_yes_no("Вопрос? Да/Нет")) is expected


@pytest.mark.parametrize(
    "answers, expected", [(["по возрастанию"], False), (["По убыванию"], True), (["вбок", "убыванию"], True)]
)
def test_ask_sort_reverse(answers: list[str], expected: bool) -> None:
    assert run_with_input(answers, ask_sort_reverse) is expected


def test_format_transaction(transactions: list[dict[str, Any]]) -> None:
    assert format_transaction(transactions[3]) == (
        "19.08.2018 Перевод с карты на карту\n"
        "Visa Classic 6831 98** **** 7658 -> Visa Platinum 8990 92** **** 5229\n"
        "Сумма: 56883.54 USD"
    )
    assert format_transaction(transactions[2]).endswith("Сумма: 43318.34 руб.")


def test_format_transaction_without_from() -> None:
    transaction = {
        "date": "2019-12-08T22:46:21.935582",
        "description": "Открытие вклада",
        "operationAmount": {"amount": "40542", "currency": {"name": "руб.", "code": "RUB"}},
        "to": "Счет 90424923579946435907",
    }
    assert format_transaction(transaction) == "08.12.2019 Открытие вклада\nСчет **5907\nСумма: 40542 руб."


def test_main_prints_filtered_transactions(
    capsys: pytest.CaptureFixture[str], transactions: list[dict[str, Any]]
) -> None:
    answers = ["1", "executed", "да", "по возрастанию", "нет", "да", "перевод"]
    with patch.dict("src.main.FILE_SOURCES", {"1": ("JSON", lambda path: transactions, "operations.json")}):
        run_with_input(answers, main)

    output = capsys.readouterr().out
    assert "Всего банковских операций в выборке: 4" in output
    dates = ["30.06.2018", "19.08.2018", "23.03.2019", "04.04.2019"]
    positions = [output.index(date) for date in dates]
    assert positions == sorted(positions)


def test_main_only_rub(capsys: pytest.CaptureFixture[str], transactions: list[dict[str, Any]]) -> None:
    answers = ["1", "EXECUTED", "нет", "да", "нет"]
    with patch.dict("src.main.FILE_SOURCES", {"1": ("JSON", lambda path: transactions, "operations.json")}):
        run_with_input(answers, main)

    output = capsys.readouterr().out
    assert "Всего банковских операций в выборке: 1" in output
    assert "Сумма: 43318.34 руб." in output


def test_main_empty_result(capsys: pytest.CaptureFixture[str], transactions: list[dict[str, Any]]) -> None:
    answers = ["2", "pending", "нет", "нет", "нет"]
    with patch.dict("src.main.FILE_SOURCES", {"2": ("CSV", lambda path: transactions, "transactions.csv")}):
        run_with_input(answers, main)

    assert "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации" in capsys.readouterr().out
