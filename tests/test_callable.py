import warnings
from functools import partial
from unittest.mock import MagicMock

from ftools.callable import (
    fullname,
    rename,
    identity,
    deprecated,
    curry,
    currymethod,
    flow,
    noop,
    constant,
    graceful,
    once,
    star,
)


def test_fullname():
    assert fullname(partial) == "functools.partial"


def test_rename():
    @rename("g")
    def f(x):
        return x

    assert f.__name__ == "g"


def test_identity():
    assert identity(1) == 1


def test_deprecated():
    @deprecated
    def f(x):
        return x

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        f(42)
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "tests.test_callable.f is deprecated" == str(w[-1].message)


def test_curry():
    def f(x):
        return x * 2

    assert curry(f).__name__ is "f"
    assert curry(f)(2) is 4

    def g(x, y):
        return x * 2 + y

    assert isinstance(curry(g)(2), partial)
    assert curry(g)(2, 3) is 7

    @curry
    def h(x, y, z=0):
        return x * y * z

    assert h(1, 2, 3) == 6
    assert h(1, 2) == 0
    assert h(1)(2) == 0
    assert h(1)(2, z=3) == 6
    assert h(1, z=3)(2) == 6


def test_currymethod():
    class A:
        @currymethod
        def b(self, c, d, e):
            return self, c, d, e

    a = A()

    assert A.b(1, 2, a, e=3) == (a, 1, 2, 3)
    assert A.b(1)(2, a, e=3) == (a, 1, 2, 3)
    assert A.b(1, 2, e=3)(a) == (a, 1, 2, 3)
    assert a.b(1, 2, e=3) == (a, 1, 2, 3)
    assert a.b(1, e=3)(2) == (a, 1, 2, 3)
    assert a.b(1)(2, e=3) == (a, 1, 2, 3)


def test_flow():
    f = flow((lambda n: n * 2, str,))
    assert f(4) == str(4 * 2)


def test_noop():
    assert noop() is None
    assert noop(1, 2, 3) is None


def test_constant():
    assert constant(4)() is 4
    assert constant(4)(1, 2, 3) is 4


def test_graceful():
    def f():
        raise RuntimeError("Check check, 1, 1")

    graceful_f = graceful(f)
    try:
        f()
    except Exception as e:
        assert e
    assert graceful_f() is None


def test_once():
    f = MagicMock()
    once_f = once(f)
    once_f()
    once_f()
    f.assert_called_once()


def test_star():
    args = [2, 2]

    def f(x, y):
        return x * y

    result = star(f)(args)
    assert result == 4
