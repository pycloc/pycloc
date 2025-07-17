from pathlib import Path
from typing import Any, List

from pytest import mark, param, raises

# noinspection PyProtectedMember
from pycloc.command import serialize


@mark.parametrize(
    "value,expected",
    [
        param(None, [], id="none"),
        param(False, [], id="false"),
        param(True, ["--name"], id="true"),
        param(3, ["--name=3"], id="integer"),
        param(3.14, ["--name=3.14"], id="float"),
        param("value", ["--name=value"], id="string"),
        param(("a", "b", "c"), ["--name=a,b,c"], id="tuple"),
        param([1, 2, 3], ["--name=1", "--name=2", "--name=3"], id="list"),
        param({1, 2, 3}, ["--name=1", "--name=2", "--name=3"], id="set"),
        param(Path("/path/to/file"), ["--name=/path/to/file"], id="path"),
    ],
)
def test_serialization(value: Any, expected: List[str]):
    actual = serialize(name="name", value=value)
    assert expected == actual


@mark.parametrize(
    "value,expected",
    [
        param(tuple(), [], id="tuple"),
        param(list(), [], id="list"),
        param(set(), [], id="set"),
        param(0, ["--name=0"], id="integer"),
        param(0.0, ["--name=0.0"], id="float"),
    ],
)
def test_serialization_empty(value: Any, expected: List[str]):
    actual = serialize(name="name", value=value)
    assert expected == actual


@mark.parametrize(
    "name",
    [
        param("", id="empty"),
        param(" ", id="blank"),
        param("\n", id="newline"),
        param("\t", id="tab"),
        param("~", id="symbol"),
        param("a b", id="words"),
        param("a\nb", id="lines"),
        param("a\tb", id="columns"),
        param("a,b", id="comma"),
        param("пупупум", id="cyrillic"),
    ],
)
def test_serialization_name_error(name: str):
    with raises(ValueError) as error:
        serialize(name=name, value=None)
    assert str(error.value).lower().startswith("invalid name")


@mark.parametrize(
    "value",
    [
        param(5 + 3j, id="complex"),
        param(type, id="type"),
        param(object(), id="object"),
        param(Exception(), id="exception"),
        param(range(0, 10), id="range"),
        param(lambda x: x, id="function"),
        param((_ for _ in []), id="generator"),
    ],
)
def test_serialization_type_error(value: Any):
    with raises(TypeError) as error:
        serialize(name="name", value=value)
    assert str(error.value).lower().startswith("invalid type")
