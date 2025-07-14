from subprocess import CalledProcessError
from typing import Type, TypeVar

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
    pass


class CLOCArgumentError(CLOCError):
    pass


class CLOCArgumentNameError(CLOCArgumentError, ValueError):
    def __init__(self, name: str):
        self._name: str = name

    def __str__(self):
        return f"Invalid name: '{self.name}'"

    @property
    def name(self) -> str:
        return self._name


class CLOCArgumentTypeError(CLOCArgumentError, TypeError):
    def __init__(self, value: T):
        self._type: Type[T] = type(value)

    def __str__(self):
        return f"Invalid type: '{self.type.__name__}'"

    @property
    def type(self) -> Type[T]:
        return self._type


class CLOCCommandError(CLOCError, CalledProcessError):
    pass


class CLOCDependencyError(CLOCError, OSError):
    pass
