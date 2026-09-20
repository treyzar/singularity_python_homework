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
