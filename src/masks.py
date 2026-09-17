CARD_NUMBER_LENGTH = 16
ACCOUNT_MIN_LENGTH = 4


def get_mask_card_number(card_number: str) -> str:
    digits = str(card_number).strip()
    if len(digits) != CARD_NUMBER_LENGTH or not digits.isdigit():
        raise ValueError("Номер карты должен состоять из 16 цифр")

    masked = f"{digits[:6]}{'*' * 6}{digits[-4:]}"
    return " ".join(masked[index : index + 4] for index in range(0, CARD_NUMBER_LENGTH, 4))


def get_mask_account(account_number: str) -> str:
    digits = str(account_number).strip()
    if len(digits) < ACCOUNT_MIN_LENGTH or not digits.isdigit():
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    return f"**{digits[-4:]}"


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))
