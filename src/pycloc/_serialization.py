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
        case float() | int() | PathLike():
            return [f"{flag}={value}"]
        case str():
            return [f"{flag}={value}"] if value else []
        case bytearray() | bytes():
            return [f"{flag}={decoded}"] if (decoded := value.decode()) else []
        case tuple():
            return [f"{flag}={values}"] if (values := ",".join(map(str, value))) else []
        case list() | set():
            return sum([[f"{flag}={value}"] for value in value], [])
        case _:
            raise CLOCArgumentTypeError(value)
