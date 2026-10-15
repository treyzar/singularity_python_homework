import logging
from pathlib import Path

CARD_NUMBER_LENGTH = 16
ACCOUNT_MIN_LENGTH = 4

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(LOGS_DIR / "masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Return a masked card number in the format ``XXXX XX** **** XXXX``."""
    logger.debug("Маскирование номера карты")
    digits = str(card_number).strip()
    if len(digits) != CARD_NUMBER_LENGTH or not digits.isdigit():
        logger.error("Некорректный номер карты: ожидается 16 цифр, получено %d символов", len(digits))
        raise ValueError("Номер карты должен состоять из 16 цифр")

    masked = f"{digits[:6]}{'*' * 6}{digits[-4:]}"
    result = " ".join(masked[index : index + 4] for index in range(0, CARD_NUMBER_LENGTH, 4))
    logger.info("Номер карты замаскирован: %s", result)
    return result


def get_mask_account(account_number: str) -> str:
    """Return a masked account number in the format ``**XXXX``."""
    logger.debug("Маскирование номера счета")
    digits = str(account_number).strip()
    if len(digits) < ACCOUNT_MIN_LENGTH or not digits.isdigit():
        logger.error("Некорректный номер счета: ожидается минимум 4 цифры, получено %d символов", len(digits))
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    result = f"**{digits[-4:]}"
    logger.info("Номер счета замаскирован: %s", result)
    return result


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))
