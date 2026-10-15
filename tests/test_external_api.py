from typing import Any
from unittest.mock import Mock, patch

import pytest
import requests

from src.external_api import API_URL, convert_to_rub


def make_transaction(amount: str, currency: str) -> dict[str, Any]:
    return {"operationAmount": {"amount": amount, "currency": {"name": currency, "code": currency}}}


@patch("src.external_api.requests.get")
def test_convert_to_rub_returns_rub_amount_without_request(mock_get: Mock) -> None:
    assert convert_to_rub(make_transaction("31957.58", "RUB")) == 31957.58
    mock_get.assert_not_called()


@pytest.mark.parametrize("currency", ["USD", "EUR"])
@patch.dict("os.environ", {"API_KEY": "test_key"})
@patch("src.external_api.requests.get")
def test_convert_to_rub_converts_foreign_currency(mock_get: Mock, currency: str) -> None:
    mock_get.return_value.json.return_value = {"success": True, "result": 822137.5}

    result = convert_to_rub(make_transaction("8221.37", currency))

    assert result == 822137.5
    assert isinstance(result, float)
    mock_get.assert_called_once_with(
        API_URL,
        headers={"apikey": "test_key"},
        params={"from": currency, "to": "RUB", "amount": 8221.37},
        timeout=10,
    )


@patch("src.external_api.requests.get")
def test_convert_to_rub_raises_on_http_error(mock_get: Mock) -> None:
    mock_get.return_value.raise_for_status.side_effect = requests.HTTPError("401 Unauthorized")

    with pytest.raises(requests.HTTPError):
        convert_to_rub(make_transaction("100", "USD"))
