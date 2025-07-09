from os import PathLike
from re import Pattern
from re import compile as pattern
from subprocess import CalledProcessError
from typing import List, Optional

from pycloc._aliases import AnyPath, Flags, FlagValue
from pycloc._subprocess import run
from pycloc._utils import is_property
from pycloc.exceptions import CLOCArgumentNameError, CLOCArgumentTypeError, CLOCCommandError

__all__ = ("CLOC",)

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


class CLOC:
    def __init__(self, workdir: Optional[AnyPath] = None, **flags: FlagValue):
        self._executable: AnyPath = "cloc"
        self._workdir: Optional[AnyPath] = workdir
        self._flags: Flags = flags

    @property
    def executable(self) -> AnyPath:
        return self._executable

    @executable.setter
    def executable(self, value: AnyPath):
        self._executable = value

    @property
    def workdir(self) -> Optional[AnyPath]:
        return self._workdir

    @workdir.setter
    def workdir(self, value: Optional[AnyPath]):
        self._workdir = value

    def __delattr__(self, name: str):
        del self._flags[name]

    def __getattr__(self, name: str) -> FlagValue:
        return self._flags[name]

    def __setattr__(self, name: str, value: FlagValue):
        if is_property(self, name) or name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._flags[name] = value

    def __call__(
        self,
        argument: AnyPath,
        *arguments: AnyPath,
        workdir: Optional[AnyPath] = None,
        **flags: FlagValue,
    ) -> str:
        executable = self.executable
        workdir = self.workdir or workdir
        flags = self._flags.copy() | flags
        try:
            return run(
                executable=executable,
                cwd=workdir,
                arguments=[argument, *arguments],
                flags=[
                    serialized
                    for name, value in flags.items()
                    if value is not None
                    for serialized in serialize(
                        name=name,
                        value=value,
                    )
                ],
            )
        except CalledProcessError as ex:
            raise CLOCCommandError(
                cmd=ex.cmd,
                returncode=ex.returncode,
                output=ex.output,
                stderr=ex.stderr,
            ) from None
        except FileNotFoundError as ex:
            raise CLOCCommandError(
                cmd=ex.filename,
                returncode=127,
                stderr=ex.strerror,
            ) from ex
