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

## Декоратор log

Модуль `src/decorators.py` содержит декоратор `log`, который логирует результат
вызова функции. Если передан необязательный аргумент `filename`, логи
дописываются в этот файл, иначе выводятся в консоль. При ошибке записывается
имя функции, тип ошибки и входные параметры, а исключение пробрасывается дальше.

```python
from src.decorators import log


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


my_function(1, 2)
# в mylog.txt: my_function ok
# при ошибке:  my_function error: TypeError. Inputs: (1, 'a'), {}


@log()
def divide(x, y):
    return x / y


divide(1, 2)  # в консоль: divide ok
```

## Работа с JSON и конвертация валют

Файл с операциями лежит в `data/operations.json`.

Модуль `src/utils.py` — функция `get_transactions(path)` читает JSON-файл и
возвращает список транзакций. Если файл не найден, пустой или содержит не
список, возвращается пустой список.

Модуль `src/external_api.py` — функция `convert_to_rub(transaction)`
возвращает сумму транзакции в рублях (`float`). Суммы в USD и EUR
конвертируются по текущему курсу через
[Exchange Rates Data API](https://apilayer.com/marketplace/exchangerates_data-api).

```python
from src.external_api import convert_to_rub
from src.utils import get_transactions

transactions = get_transactions("data/operations.json")
print(convert_to_rub(transactions[1]))
```

Для работы конвертации скопируйте шаблон `.env.example` в `.env` и укажите
свой ключ API:

```
API_KEY=ваш_ключ
```

## Логирование

Модули `masks` и `utils` пишут логи в папку `logs/` в корне проекта:
`logs/masks.log` и `logs/utils.log`. Папка создается автоматически, а файлы
перезаписываются при каждом запуске. Формат записи:

```
2026-10-11 09:19:44,971 - utils - ERROR - Файл nope.json не найден
```

Успешные вызовы пишутся с уровнями DEBUG и INFO, ошибки с уровнем ERROR.

## Чтение CSV и XLSX

Теперь транзакции можно брать не только из JSON, но и из CSV- и XLSX-файлов.
Файлы лежат в папке `data/`: `transactions.csv` и `transactions_excel.xlsx`.

Модуль `src/readers.py` читает их с помощью `pandas`:

- `read_transactions_from_csv(path)` — читает CSV-файл с разделителем `;`;
- `read_transactions_from_excel(path)` — читает XLSX-файл.

Обе функции принимают путь к файлу и возвращают список словарей с
транзакциями. Формат такой же, как в JSON-файле: сумма и валюта лежат во
вложенном словаре `operationAmount`. Пустые строки пропускаются. Если файла
нет, возвращается пустой список.

```python
from src.readers import read_transactions_from_csv, read_transactions_from_excel

transactions = read_transactions_from_csv("data/transactions.csv")
print(len(transactions))  # 999
print(transactions[0]["description"])  # Перевод организации

transactions = read_transactions_from_excel("data/transactions_excel.xlsx")
```

## Поиск и подсчет операций

В модуле `src/processing.py` есть еще две функции:

- `process_bank_search(data, search)` — возвращает операции, в описании
  которых встречается строка `search`. Поиск выполняется регулярным выражением
  (библиотека `re`) без учета регистра.
- `process_bank_operations(data, categories)` — считает с помощью
  `collections.Counter` количество операций по категориям из поля
  `description` и возвращает словарь `{категория: количество}`.

```python
from src.processing import process_bank_operations, process_bank_search
from src.utils import get_transactions

transactions = get_transactions("data/operations.json")
process_bank_search(transactions, "перевод")
process_bank_operations(transactions, ["Перевод организации", "Открытие вклада"])
# {'Перевод организации': 40, 'Открытие вклада': 10}
```

## Запуск программы

Функция `main` в модуле `src/main.py` связывает все части проекта в
консольную программу:

```bash
poetry run python -m src.main
```

Программа предлагает выбрать файл с транзакциями (JSON, CSV или XLSX), затем
статус операций (`EXECUTED`, `CANCELED`, `PENDING`, регистр не важен; при
неверном статусе запрос повторяется), сортировку по дате, вывод только рублевых
транзакций и поиск по слову в описании. В конце печатается количество
найденных операций и их список:

```
Всего банковских операций в выборке: 2

08.12.2019 Открытие вклада
Счет **5907
Сумма: 40542 руб.

12.11.2019 Перевод с карты на карту
MasterCard 7771 27** **** 3727 -> Visa Platinum 1293 38** **** 9203
Сумма: 130 USD
```

Если под условия не подошла ни одна операция, программа сообщает об этом.

## Тестирование

Тесты написаны на `pytest` и лежат в директории `tests/`: для каждого модуля
из `src/` есть отдельный файл (`test_masks.py`, `test_widget.py`,
`test_processing.py`, `test_readers.py`, `test_main.py`). Общие тестовые данные вынесены в фикстуры в
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
покрытие кода в `src/` — 95%.
