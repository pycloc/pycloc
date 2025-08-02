from doctest import testmod as doctest
from types import ModuleType

from pytest import mark, param

from pycloc import command, exceptions


@mark.parametrize(
    "module",
    [
        param(command, id=command.__name__),
        param(exceptions, id=exceptions.__name__),
    ],
)
def test_documentation_examples(module: ModuleType):
    result = doctest(module, verbose=True)
    assert result.failed == 0, f"Doctest failures in {module.__name__}: {result.failed}"
