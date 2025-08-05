"""
Core classes used for interfacing with ``cloc``.

Classes:
    CLOC: Provides a convenient interface to create and execute ``cloc`` commands.
"""

from subprocess import CalledProcessError
from typing import Literal, Optional, overload

from pycloc._aliases import AnyPath, CommandOutput, Flags, FlagValue
from pycloc._properties import properties
from pycloc._resources import script
from pycloc._subprocess import perl, run
from pycloc._utils import is_property
from pycloc.exceptions import CLOCCommandError, CLOCDependencyError

__all__ = ("CLOC",)


class CLOC:
    """
    Provides a convenient interface to create and execute ``cloc``
    commands with dynamic flag handling and proper error management.
    Flags can be set as attributes or passed during initialization and execution.

    Args:
        workdir: Optional working directory for executing the command.
        encoding: Optional text encoding for parsing output.
        errors: Optional error handling strategy for encoding issues.
        **flags: Initial set of command-line flags that will be applied.
    """

    __version__ = properties.version
    """Current version of ``cloc``."""

    def __init__(
        self,
        *,
        workdir: Optional[AnyPath] = None,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        **flags: FlagValue,
    ):
        self._workdir: Optional[AnyPath] = workdir
        self._encoding: Optional[str] = encoding
        self._errors: Optional[str] = errors
        self._flags: Flags = flags

    @property
    def workdir(self) -> Optional[AnyPath]:
        return self._workdir

    @workdir.setter
    def workdir(self, value: Optional[AnyPath]):
        self._workdir = value

    @property
    def encoding(self) -> Optional[str]:
        return self._encoding

    @encoding.setter
    def encoding(self, value: Optional[str]):
        self._encoding = value

    @property
    def errors(self) -> Optional[str]:
        return self._errors

    @errors.setter
    def errors(self, value: Optional[str]):
        self._errors = value

    def __delattr__(self, name: str):
        del self._flags[name]

    def __getattr__(self, name: str) -> FlagValue:
        return self._flags[name]

    def __setattr__(self, name: str, value: FlagValue):
        if is_property(self, name) or name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._flags[name] = value

    @overload
    def __call__(
        self,
        argument: AnyPath,
        /,
        *arguments: AnyPath,
        asynchronous: Literal[False] = False,
        workdir: Optional[AnyPath] = None,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        **flags: FlagValue,
    ) -> str: ...

    @overload
    async def __call__(
        self,
        argument: AnyPath,
        /,
        *arguments: AnyPath,
        asynchronous: Literal[True] = True,
        workdir: Optional[AnyPath] = None,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        **flags: FlagValue,
    ) -> str: ...

    def __call__(
        self,
        argument: AnyPath,
        /,
        *arguments: AnyPath,
        asynchronous: bool = False,
        workdir: Optional[AnyPath] = None,
        encoding: Optional[str] = None,
        errors: Optional[str] = None,
        **flags: FlagValue,
    ) -> CommandOutput:
        """
        Execute ``cloc`` command with the specified arguments and flags.

        Args:
            argument: Required positional argument to pass to the command.
            *arguments: Additional positional arguments to pass to the command.
            asynchronous: Whether to execute the command asynchronously.
            workdir: Optional working directory for this execution.
            encoding: Optional text encoding for parsing output.
            errors: Optional error handling strategy for encoding issues.
            **flags: Additional command-line flags for this execution only.

        Returns:
            Output from the ``cloc`` command, either as a string or as an ``Awaitable`` string.

        Note:
            Warning messages from the output are logged but will not result in a raised exception.

        Raises:
            CLOCDependencyError: If [Perl](https://www.perl.org) is not available on the system.
            CLOCCommandError: If the ``cloc`` command fails or returns non-zero exit code.

        Examples:
            >>> import json
            >>> from tempfile import NamedTemporaryFile
            >>> from pycloc import CLOC
            >>> with NamedTemporaryFile(suffix=".md", mode="w") as buffer:
            ...     _ = buffer.write("Hello, CLOC!")
            ...     buffer.flush()
            ...     cloc = CLOC(json=True)
            ...     output = cloc(buffer.name)
            ...     result = json.loads(output)
            ...     result["Markdown"]["code"]
            1
        """
        if not perl():
            raise CLOCDependencyError("Perl is not available!")
        try:
            return run(
                executable=script(),
                cwd=(self.workdir or workdir),
                arguments=[argument, *arguments],
                flags=(self._flags.copy() | flags).items(),
                encoding=(self.encoding or encoding),
                errors=(self.errors or errors),
                asynchronous=asynchronous,
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
