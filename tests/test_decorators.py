from pathlib import Path
from typing import Any

import pytest

from src.decorators import log


@pytest.fixture
def log_file(tmp_path: Path) -> Path:
    return tmp_path / "mylog.txt"


def test_log_to_console_success(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def add(x: int, y: int) -> int:
        return x + y

    assert add(1, 2) == 3
    assert capsys.readouterr().out == "add ok\n"


@pytest.mark.parametrize(
    "args, kwargs, expected_inputs",
    [
        ((1, 0), {}, "(1, 0), {}"),
        ((1,), {"y": 0}, "(1,), {'y': 0}"),
        ((), {"x": 5, "y": 0}, "(), {'x': 5, 'y': 0}"),
    ],
)
def test_log_to_console_error(
    capsys: pytest.CaptureFixture[str], args: tuple[Any, ...], kwargs: dict[str, Any], expected_inputs: str
) -> None:
    @log()
    def divide(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(*args, **kwargs)
    assert capsys.readouterr().out == f"divide error: ZeroDivisionError. Inputs: {expected_inputs}\n"


def test_log_to_file_success(log_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
    @log(filename=str(log_file))
    def my_function(x: int, y: int) -> int:
        return x + y

    assert my_function(1, 2) == 3
    assert log_file.read_text(encoding="utf-8") == "my_function ok\n"
    assert capsys.readouterr().out == ""


def test_log_to_file_error(log_file: Path) -> None:
    @log(filename=str(log_file))
    def my_function(x: int, y: int) -> int:
        raise ValueError("ошибка")

    with pytest.raises(ValueError, match="ошибка"):
        my_function(1, 2)
    assert log_file.read_text(encoding="utf-8") == "my_function error: ValueError. Inputs: (1, 2), {}\n"


def test_log_appends_to_file(log_file: Path) -> None:
    @log(filename=str(log_file))
    def my_function(x: int) -> int:
        return x

    my_function(1)
    my_function(2)
    assert log_file.read_text(encoding="utf-8") == "my_function ok\nmy_function ok\n"


def test_log_keeps_function_metadata() -> None:
    @log()
    def documented() -> None:
        """Docstring."""

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "Docstring."
