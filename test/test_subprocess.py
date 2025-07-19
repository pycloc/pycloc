from textwrap import dedent
from typing import cast

from pytest import raises
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


def test_warnings(mocker: MockFixture):
    expected = "{}"
    warnings = dedent("""
    1 error:
    Unable to read: 1
    """)
    mock_result = mocker.Mock()
    mock_result.stdout = expected
    mock_result.stderr = warnings

    subprocess = mocker.patch(
        target="subprocess.run",
        return_value=mock_result,
    )
    logger = mocker.patch(
        target="pycloc._subprocess.logger",
    )

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
    actual = [argument for call in logger.warning.call_args_list for argument in call.args]
    assert logger.warning.call_count == 2
    assert expected == actual
