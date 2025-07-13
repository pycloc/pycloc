from importlib.resources import files
from pathlib import Path
from typing import cast

from . import resources

directory = files(resources)


def metadata() -> Path:
    return cast(typ=Path, val=directory / "cloc.ini")


def script() -> Path:
    return cast(typ=Path, val=directory / "cloc.pl")
