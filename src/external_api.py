import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.apilayer.com/exchangerates_data/convert"
CONVERTIBLE_CURRENCIES = ("USD", "EUR")


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """Return the transaction amount in rubles.

    Amounts in USD and EUR are converted at the current rate received from
    the Exchange Rates Data API. Amounts in other currencies are returned
    as is.
    """
    operation_amount = transaction["operationAmount"]
    amount = float(operation_amount["amount"])
    currency = operation_amount["currency"]["code"]

    if currency not in CONVERTIBLE_CURRENCIES:
        return amount

    response = requests.get(
        API_URL,
        headers={"apikey": os.getenv("API_KEY", "")},
        params={"from": currency, "to": "RUB", "amount": amount},
        timeout=10,
    )
    response.raise_for_status()
    return float(response.json()["result"])
