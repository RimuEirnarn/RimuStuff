"""utils"""
from datetime import datetime
from functools import wraps
from platform import python_version, system as osname_f
from platform import version as osversion_f
from traceback import format_exception
from types import TracebackType
from typing import Any, Callable, Iterable, TextIO, Type

from tomllib import loads as _load

PROJECT_VERSION = "0.0.2"

EXC_FORMAT = """
{header}

{content}

{footer}
"""


def load(file: "TextIO", **kwargs) -> 'dict[str, Any]':
    """Load toml data"""
    return _load(file.read(), **kwargs)


def usage_cache(used=10):
    """Usage function"""
    data = {}

    def wrapper0(func):
        @wraps(func)  # type: ignore
        def wrapper(*args, **kwargs):
            if data.get(func, None) is None:
                data[func] = [func(*args, **kwargs), used]
                return data[func][0]
            if data[func][1] == 0:
                data[func] = [func(*args, **kwargs), used]
                return data[func][0]
            return data[func][0]
        return wrapper
    return wrapper0


class CallAwait:
    """Used in `fn_partial`, when this passed, function"""

    def __init__(self, __callable: Callable) -> None:
        self._callable = __callable

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self._callable(*args, **kwds)

    def __repr__(self) -> str:
        return "CallAwait"


def has_common_item(list1: Iterable[Any], list2: Iterable[Any]) -> bool:
    """Are some iterable have common item?

    Args:
        list1 (Iterable[Any]): Iterable 1
        list2 (Iterable[Any]): Iterable 2

    Returns:
        bool: True if both array has common item.
    """
    return any(item in list2 for item in list1)

# Bootstrap related


def save_traceback(exc: Type[BaseException],
                   value: BaseException,
                   traceback: TracebackType) -> str:
    """Save traceback as text"""
    return "".join(format_exception(exc, value, traceback))


def save_to_file_error(filename: str,
                       exc: BaseException,
                       is_append=False,
                       bootstrap_id: int | None = None):
    """Save an error to a file"""
    mode = "w" if not is_append else 'a'
    with open(filename, mode, encoding='utf-8') as file:
        header = f"{str(bootstrap_id or 1):=^25}"
        content = save_traceback(
            type(exc), exc, exc.__traceback__)  # type: ignore
        footer = f"{'':=>25}"
        return file.write(EXC_FORMAT.format(header=header, content=content, footer=footer))


def save_exc_groups(filename: str,
                    exc: BaseExceptionGroup):
    """Save all errors to file"""
    bwrites = 0
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"""\
Occurred At      : {datetime.today():%c}
System           : {osname_f()}/{osversion_f()}
System Name      : {osname_f()}
System Version   : {osversion_f()}
Python Version   : Python{python_version()}
RimuStuff Version: {PROJECT_VERSION}""")

        header = f"{'':=^25}"
        content = save_traceback(
        type(exc), exc, exc.__traceback__)  # type: ignore
        footer = f"{'':=>25}"
        bwrites += file.write(EXC_FORMAT.format(header=header,
                              content=content, footer=footer))
