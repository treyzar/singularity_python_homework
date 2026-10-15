import json
import logging
from pathlib import Path
from typing import Any

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOGS_DIR / "utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_transactions(path: str) -> list[dict[str, Any]]:
    """Return a list of financial transactions loaded from a JSON file.

    An empty list is returned if the file is not found, is empty, contains
    invalid JSON or its top-level value is not a list.
    """
    logger.debug("Чтение транзакций из файла %s", path)
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error("Файл %s не найден", path)
        return []
    except json.JSONDecodeError as error:
        logger.error("Файл %s пустой или содержит некорректный JSON: %s", path, error)
        return []

    if not isinstance(data, list):
        logger.error("Файл %s содержит %s вместо списка", path, type(data).__name__)
        return []

    logger.info("Из файла %s загружено транзакций: %d", path, len(data))
    return data
