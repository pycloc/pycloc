from pathlib import Path
from tempfile import NamedTemporaryFile

from pytest import fixture, mark, param, raises
from pytest_lazy_fixtures import lf as lazy_fixture
from pytest_mock import MockFixture

from pycloc import CLOC, CLOCCommandError, CLOCDependencyError


@fixture
def missing_script(tmp_path: Path):
    with NamedTemporaryFile(
        mode="w+",
        dir=tmp_path,
        prefix="missing-",
        suffix=".pl",
    ) as buffer:
        return Path(buffer.name)


@fixture
def empty_script(tmp_path: Path):
    with NamedTemporaryFile(
        mode="w+",
        dir=tmp_path,
        prefix="empty-",
        suffix=".pl",
    ) as buffer:
        yield Path(buffer.name)


def test_no_perl(mocker: MockFixture, tmp_path: Path):
    perl = mocker.patch(
        target="pycloc.command.perl",
        return_value=None,
    )
    with raises(CLOCDependencyError):
        cloc = CLOC()
        cloc(tmp_path)
    perl.assert_called_once()


@mark.parametrize(
    "path",
    [
        param(lazy_fixture("missing_script"), id="missing"),
        param(lazy_fixture("empty_script"), id="empty"),
    ],
)
def test_script_issues(
    mocker: MockFixture,
    tmp_path: Path,
    path: Path,
):
    script = mocker.patch(
        target="pycloc.command.script",
        return_value=path,
    )
    with raises(CLOCCommandError) as error:
        cloc = CLOC()
        cloc(tmp_path)
    script.assert_called_once()
    assert error.value.returncode == 127
