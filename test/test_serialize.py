from pathlib import Path
from typing import Any, List, TypeVar

from pytest import mark, param, raises

# noinspection PyProtectedMember
from pycloc._serialization import serialize

T = TypeVar("T")


@mark.parametrize(
    "value,expected",
    [
        param(None, [], id="none"),
        param(False, [], id="bool,false"),
        param(True, ["--name"], id="bool,true"),
        param(0, ["--name=0"], id="int,zero"),
        param(1, ["--name=1"], id="int,positive"),
        param(-1, ["--name=-1"], id="int,negative"),
        param(0.0, ["--name=0.0"], id="float,zero"),
        param(1.618, ["--name=1.618"], id="float,positive"),
        param(-1.618, ["--name=-1.618"], id="float,negative"),
        param("", ["--name=''"], id="str,empty"),
        param("cloc", ["--name=cloc"], id="str,single"),
        param("count lines of code", ["--name='count lines of code'"], id="str,multiple"),
        param(b"", ["--name=''"], id="bytes,empty"),
        param(b"cloc", ["--name=cloc"], id="bytes,single"),
        param(b"count lines of code", ["--name='count lines of code'"], id="bytes,multiple"),
        param(bytearray(b""), ["--name=''"], id="bytearray,empty"),
        param(bytearray(b"cloc"), ["--name=cloc"], id="bytearray,single"),
        param(bytearray(b"count lines of code"), ["--name='count lines of code'"], id="bytearray,multiple"),
        param(tuple(), [], id="tuple,empty"),
        param((1,), ["--name=1"], id="tuple,single"),
        param((1, 2, 3), ["--name=1", "--name=2", "--name=3"], id="tuple,multiple"),
        param(set(), [], id="set,empty"),
        param({1}, ["--name=1"], id="set,single"),
        param({1, 2, 3}, ["--name=1", "--name=2", "--name=3"], id="set,multiple"),
        param(list(), [], id="list,empty"),
        param([1], ["--name=1"], id="list,single"),
        param([1, 2, 3], ["--name=1", "--name=2", "--name=3"], id="list,multiple"),
        param(Path(), ["--name=."], id="path,cwd"),
        param(Path("/"), ["--name=/"], id="path,root"),
        param(Path("/bin"), ["--name=/bin"], id="path,single"),
        param(Path("/var/log"), ["--name=/var/log"], id="path,multiple"),
    ],
)
def test_serialization(value: T, expected: List[str]):
    assert expected == serialize(
        name="name",
        value=value,
    )


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
