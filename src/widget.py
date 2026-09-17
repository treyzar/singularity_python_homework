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


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
