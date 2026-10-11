# Bank Widget

Проект обрабатывает данные о банковских операциях клиента. В нём есть функции
для маскировки номеров карт и счетов, форматирования дат, фильтрации операций
по статусу и сортировки по дате.

## Установка

Требуется Python 3.12 и Poetry. Из корневой директории проекта выполните:

```bash
poetry install
```

## Использование

Функции обработки находятся в `src/processing.py`:

```python
from src.processing import filter_by_state, sort_by_date

operations = [
    {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
    {"id": 2, "state": "CANCELED", "date": "2024-03-10T12:00:00"},
]

# По умолчанию оставляет только операции со статусом EXECUTED.
executed_operations = filter_by_state(operations)

# По умолчанию сортирует от новых операций к старым.
sorted_operations = sort_by_date(executed_operations)

# Для сортировки от старых операций к новым передайте reverse=False.
ascending_operations = sort_by_date(operations, reverse=False)
```

`filter_by_state` принимает список операций и необязательный статус `state`.
`sort_by_date` принимает список операций и необязательный флаг `reverse`.
Обе функции возвращают новый список и не изменяют исходный.

## Генераторы

Модуль `src/generators.py` содержит функции для работы с большими списками
транзакций без создания промежуточных списков.

```python
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

# Итератор по транзакциям в заданной валюте (по коду валюты, например USD).
usd_transactions = filter_by_currency(transactions, "USD")
print(next(usd_transactions))

# Генератор описаний операций по очереди.
descriptions = transaction_descriptions(transactions)
print(next(descriptions))  # Перевод организации

# Генератор номеров карт от start до stop включительно.
for card_number in card_number_generator(1, 3):
    print(card_number)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
```

`filter_by_currency` принимает список транзакций и код валюты, возвращает
итератор. `transaction_descriptions` принимает список транзакций и по запросу
выдает поле `description`. `card_number_generator` принимает границы диапазона
от 1 до 9999999999999999 и выдает номера в формате `XXXX XXXX XXXX XXXX`; при
некорректных границах выбрасывает `ValueError`.

## Тестирование

Тесты написаны на `pytest` и лежат в директории `tests/`: для каждого модуля
из `src/` есть отдельный файл (`test_masks.py`, `test_widget.py`,
`test_processing.py`). Общие тестовые данные вынесены в фикстуры в
`tests/conftest.py`, а разные входные данные проверяются через
`@pytest.mark.parametrize`.

Запуск тестов:

```bash
poetry run pytest
```

Запуск тестов с оценкой покрытия и генерацией HTML-отчета:

```bash
poetry run pytest --cov=src --cov-report=html
```

Отчет появится в папке `htmlcov/` (откройте `htmlcov/index.html`). Текущее
покрытие кода в `src/` — 89%.
