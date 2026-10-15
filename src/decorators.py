import functools
from typing import Any, Callable


def log(filename: str | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Return a decorator that logs the result of a function call.

    On success ``<name> ok`` is logged, on failure
    ``<name> error: <error type>. Inputs: <args>, <kwargs>`` is logged and the
    exception is raised again. Logs are appended to ``filename`` if it is given,
    otherwise they are printed to the console.
    """

    def write(message: str) -> None:
        """Write a log message to the file or to the console."""
        if filename:
            with open(filename, "a", encoding="utf-8") as file:
                file.write(message + "\n")
        else:
            print(message)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Wrap ``func`` so that its calls are logged."""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Call ``func`` and log the outcome."""
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                write(f"{func.__name__} error: {type(error).__name__}. Inputs: {args}, {kwargs}")
                raise
            write(f"{func.__name__} ok")
            return result

        return wrapper

    return decorator


if __name__ == "__main__":

    @log()
    def add(x: int, y: int) -> int:
        """Add two numbers."""
        return x + y

    add(1, 2)
