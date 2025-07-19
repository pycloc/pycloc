from os import PathLike
from re import Pattern
from re import compile as pattern
from shlex import quote
from typing import List, Optional

from pycloc._aliases import FlagValue
from pycloc.exceptions import CLOCArgumentNameError, CLOCArgumentTypeError

# language=pythonregexp
validator: Pattern[str] = pattern(r"^[a-zA-Z0-9_-]+$")


def serialize(
    name: str,
    value: FlagValue,
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
) -> List[str]:
    if not validator.match(name):
        raise CLOCArgumentNameError(name)
    flag = "--" + name.replace("_", "-")
    match value:
        case None:
            return []
        case bool():
            return [flag] if value else []
        case float() | int() | PathLike():
            serialized = str(value)
            quoted = quote(serialized)
            return [f"{flag}={quoted}"]
        case str():
            quoted = quote(value)
            return [f"{flag}={quoted}"]
        case bytearray() | bytes():
            decoded = value.decode(
                encoding=encoding if encoding else "utf-8",
                errors=errors if errors else "strict",
            )
            quoted = quote(decoded)
            return [f"{flag}={quoted}"]
        case tuple():
            values = ",".join(map(str, value))
            quoted = quote(values)
            return [f"{flag}={quoted}"]
        case list() | set():
            return [f"{flag}={quote(str(value))}" for value in value]
        case _:
            raise CLOCArgumentTypeError(value)
