from fptools.callable import curry, currymethod, flow, noop, constant, graceful
from functools import partial


def test_curry():
    def f(x):
        return x * 2

    assert curry(f).__name__ is 'f'
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
    f = flow((
        lambda n: n * 2,
        str,
    ))
    assert f(4) == str(4 * 2)


def test_noop():
    assert noop() is None
    assert noop(1, 2, 3) is None


def test_constant():
    assert constant(4)() is 4
    assert constant(4)(1, 2, 3) is 4


def test_graceful():
    def f():
        raise RuntimeError('Check check, 1, 1')
    graceful_f = graceful(f)
    try:
        f()
    except Exception as e:
        assert e
    assert graceful_f() is None
