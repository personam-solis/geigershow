"""
Set global decorators to make it easier to log, time, and debug based on a users
input
"""

import argparse
import logging
from time import perf_counter
from typing import Any, Callable
import inspect
import functools


def set_logging(parser: argparse.Namespace) -> logging:
    """
    Set logging level based on the user input. This needs to be added after the
    parser object has been built.

    Args:
        parser: Fully built parser object

    Returns:
        logging object
    """
    if parser.info:
        return logging.basicConfig(level=logging.INFO)
    elif parser.debug:
        return logging.basicConfig(level=logging.DEBUG,
                   format="%(asctime)s | %(levelname)s | PID %(process)s | %(message)s",
                   datefmt="%Y%m%d %H:%M:%S")
    else:
        return logging.basicConfig(level=logging.WARNING)


def log(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to add logging to specific levels.

    Args:
        func: Any Function any Type of Args`

    Returns:
        func: same function
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logging.info(f"Calling {func.__name__}")
        value = func(*args, **kwargs)
        logging.debug(f"Function {func.__name__} info:\n    {inspect.signature(func)}")
        logging.debug(f"Function {func.__name__} param list:\n    {inspect.getargspec(func)}")
        logging.info(f"Finished {func.__name__}")
        return value

    return wrapper


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to add timing function to info log level.

    Args:
        func: Any Function any Type of Args`

    Returns:
        func: same function
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter()
        value = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        logging.info(f"Execution of '{func.__name__}' took {run_time:.3f} seconds.")
        return value

    return wrapper


if __name__ == '__main__':
    # Do nothing as it is supposed to be imported
    pass