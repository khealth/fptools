from fptools.callable import curry, flow, noop, constant, graceful
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
