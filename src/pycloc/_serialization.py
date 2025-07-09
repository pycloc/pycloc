from os import PathLike
from re import Pattern
from re import compile as pattern
from typing import List

from pycloc._aliases import FlagValue
from pycloc.exceptions import CLOCArgumentNameError, CLOCArgumentTypeError

# language=pythonregexp
validator: Pattern[str] = pattern(r"^[a-zA-Z0-9_-]+$")


def serialize(name: str, value: FlagValue) -> List[str]:
    if not validator.match(name):
        raise CLOCArgumentNameError(name)
    flag = "--" + name.replace("_", "-")
    match value:
        case None:
            return []
        case bool():
            return [flag] if value else []
        case float() | int() | str() | PathLike():
            return [f"{flag}={value}"]
        case tuple():
            values = ",".join(map(str, value))
            return [f"{flag}={values}"]
        case list() | set():
            return sum([[f"{flag}={value}"] for value in value], [])
        case _:
            raise CLOCArgumentTypeError(value)
