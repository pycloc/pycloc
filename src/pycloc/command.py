from subprocess import CalledProcessError
from typing import Optional

from pycloc._aliases import AnyPath, Flags, FlagValue
from pycloc._properties import properties
from pycloc._resources import script
from pycloc._subprocess import perl, run
from pycloc._utils import is_property
from pycloc.exceptions import CLOCCommandError, CLOCDependencyError

__all__ = ("CLOC",)


class CLOC:
    __version__ = properties.version

    def __init__(self, workdir: Optional[AnyPath] = None, **flags: FlagValue):
        self._workdir: Optional[AnyPath] = workdir
        self._flags: Flags = flags

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
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        **flags: FlagValue,
    ) -> str:
        if not perl():
            raise CLOCDependencyError("Perl is not available!")
        try:
            return run(
                executable=script(),
                cwd=(self.workdir or workdir),
                arguments=[argument, *arguments],
                flags=(self._flags.copy() | flags).items(),
                encoding=encoding,
                errors=errors,
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
