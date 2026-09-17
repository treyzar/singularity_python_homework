from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    if not info or not info.strip():
        raise ValueError("Не передана информация о карте или счете")

    words = info.split()
    if len(words) < 2:
        raise ValueError("Строка должна содержать тип и номер карты или счета")

    number = words[-1]
    name = " ".join(words[:-1])

    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return name + " " + masked_number


def get_date(date_string: str) -> str:
    date_obj = datetime.fromisoformat(date_string)
    return date_obj.strftime("%d.%m.%Y")


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(get_date("2024-03-11T02:26:18.671407"))
