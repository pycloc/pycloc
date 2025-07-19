from pytest import fixture, mark, param

# noinspection PyProtectedMember
from pycloc._utils import is_property


class Example:
    field = None

    @property
    def property(self):
        return None

    def function(self):
        pass


@fixture
def example():
    return Example()


def test_is_property(example: Example):
    assert is_property(
        instance=example,
        name="property",
    )


@mark.parametrize(
    "name",
    [
        param("field", id="field"),
        param("function", id="function"),
        param("parameter", id="nonexistent"),
    ],
)
def test_is_not_property(example: Example, name: str):
    assert not is_property(
        instance=example,
        name=name,
    )
