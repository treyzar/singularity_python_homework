from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    words = info.split()
    number = words[-1]
    name = " ".join(words[:-1])

    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return name + " " + masked_number


def get_date(date_string: str) -> str:
    date_part = date_string.split("T")[0]
    year, month, day = date_part.split("-")

    return day + "." + month + "." + year


print(mask_account_card("Visa Platinum 7000792289606361"))
print(mask_account_card("Счет 73654108430135874305"))
print(get_date("2024-03-11T02:26:18.671407"))
