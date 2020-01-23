import pytest
from ftools.optional import ignore_optional, map_optionals, is_some


def double(x: int) -> int:
    return x * 2


def test_ignore_optional():
    wrapped_f = ignore_optional(double)
    assert wrapped_f(1) == 2
    assert wrapped_f(None) is None


@pytest.mark.parametrize("iterable, expected_iterable", [
    pytest.param(
        [1, 2, 3],
        [2, 4, 6],
        id="all some"
    ),
    pytest.param(
        [None, None, None],
        [None, None, None],
        id="all none"
    ),
    pytest.param(
        [1, None, 3],
        [2, None, 6],
        id="mixed"
    ),
])
def test_map_optionals(iterable, expected_iterable):
    assert list(map_optionals(double, iterable)) == expected_iterable

@pytest.mark.parametrize("item, expected_result", [
    pytest.param(
        1,
        True
    ),
    pytest.param(
        None,
        False
    )
])
def test_is_some(item, expected_result):
    assert is_some(item) is expected_result