"""
Hierarchy of exceptions raised during the execution of the ``cloc`` command.

Classes:
    CLOCError: Base exception class for all errors related to ``cloc``.
    CLOCArgumentError: Base exception for argument-related errors in ``cloc`` execution.
    CLOCArgumentNameError: Raised when an invalid flag name is provided to ``cloc``.
    CLOCArgumentTypeError: Raised when a value of an unsupported type is specified for a flag.
    CLOCCommandError: Raised when execution of a ``cloc`` command fails.
    CLOCDependencyError: Raised when required runtime dependencies external to the Python environment are not available.
"""

from subprocess import CalledProcessError
from typing import Generic, Type, TypeVar

__all__ = (
    "CLOCArgumentNameError",
    "CLOCArgumentTypeError",
    "CLOCArgumentError",
    "CLOCCommandError",
    "CLOCDependencyError",
    "CLOCError",
)

T = TypeVar("T")


class CLOCError(Exception):
    """Base exception class for all errors related to ``cloc``."""


class CLOCArgumentError(CLOCError):
    """Base exception for argument-related errors in ``cloc`` execution."""


class CLOCArgumentNameError(CLOCArgumentError, ValueError):
    """
    Raised when an invalid flag name is provided to ``cloc``.

    Notes:
        Raised in response to a serialization error caused by an invalid flag name.
        Will not manifest as a result of an unknown flag being passed to ``cloc``.
        In those cases, a ``CLOCCommandError`` will be raised instead.

    Args:
        name: Flag name that caused the error.

    Attributes:
        name (str): Flag name that caused the error.

    Examples:
        >>> from pycloc import CLOC
        >>> cloc = CLOC()
        >>> setattr(cloc, "Flag names can't have spaces!", 0)
        >>> cloc(".")
        Traceback (most recent call last):
            ...
        pycloc.exceptions.CLOCArgumentNameError: Invalid name: 'Flag names can't have spaces!'
    """

    def __init__(self, name: str):
        self._name: str = name

    def __str__(self):
        return f"Invalid name: '{self.name}'"

    @property
    def name(self) -> str:
        return self._name


class CLOCArgumentTypeError(Generic[T], CLOCArgumentError, TypeError):
    """
    Raised when a value of an unsupported type is specified for a flag.

    Args:
        value: Value that caused the error.

    Attributes:
        type: Type of the invalid value.

    Examples:
        >>> from pycloc import CLOC
        >>> cloc = CLOC(flag=object())
        >>> cloc(".")
        Traceback (most recent call last):
            ...
        pycloc.exceptions.CLOCArgumentTypeError: Invalid type: 'object'
    """

    def __init__(self, value: T):
        self._type: Type[T] = type(value)

    def __str__(self):
        return f"Invalid type: '{self.type.__name__}'"

    @property
    def type(self) -> Type[T]:
        return self._type


class CLOCCommandError(CLOCError, CalledProcessError):
    """
    Raised when execution of a ``cloc`` command fails.

    Examples:
        >>> from pycloc import CLOCCommandError, CLOC
        >>> try:
        ...     CLOC(unsupported=1)(".")
        ... except CLOCCommandError as ex:
        ...     ex.returncode
        2
    """


class CLOCDependencyError(CLOCError, OSError):
    """
    Raised when required runtime dependencies external to the Python environment are not available.

    Notes:
        An example of an external dependency is a user-installed program or system package.
        Currently, the absence of a [Perl](https://www.perl.org) interpreter
        is the only cause for this error.
    """
