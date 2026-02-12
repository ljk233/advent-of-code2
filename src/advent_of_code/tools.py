import functools
import sys
import time
from typing import Any, Callable, Literal

from loguru import logger

PART = Literal[0, 1, 2]


logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>",
)


def solution(part: int, log_result: bool = True) -> Callable[..., Any]:
    """Decorator factory that logs execution time and results."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start_time

            part_str = "Data processed" if part == 0 else f"Part {part} executed"

            # Log with level 'INFO' for visibility
            msg = f"{part_str} in {duration:.4f}s"
            if log_result and part != 0:
                msg += f" | Result: {result}"

            logger.info(msg)

            return result

        return wrapper

    return decorator
