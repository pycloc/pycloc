from logging import WARNING
from textwrap import dedent
from typing import cast

from pytest import LogCaptureFixture, raises
from pytest_mock import MockFixture

# noinspection PyProtectedMember
from pycloc._subprocess import run


def test_no_output():
    expected = ""
    actual = run(executable="true")
    assert expected == actual


def test_output():
    expected = "Hello, CLOC!"
    actual = run(
        executable="echo",
        arguments=[expected],
    )
    assert expected == actual.strip()


def test_not_found():
    executable = "unknown"
    with raises(FileNotFoundError) as error:
        run(executable=executable)
    ex = cast(FileNotFoundError, error.value)
    assert ex.errno == 2
    assert ex.filename == executable
    assert ex.strerror == "No such file or directory"


def test_warnings(
    caplog: LogCaptureFixture,
    mocker: MockFixture,
):
    expected = "{}"
    warnings = dedent("""
    1 error:
    Unable to read: 1
    """)
    result = mocker.Mock()
    result.stdout = expected
    result.stderr = warnings

    subprocess = mocker.patch(
        target="subprocess.run",
        return_value=result,
    )
    with caplog.at_level(
        level=WARNING,
        logger="pycloc",
    ):
        actual = run(
            executable="cloc",
            arguments=["1"],
            flags=[
                ("json", True),
            ],
        )
    subprocess.assert_called_once()
    assert expected == actual

    expected = [warning for warning in warnings.splitlines() if warning]
    actual = [message for message in caplog.messages]
    assert expected == actual
