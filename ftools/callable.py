"""
Utilities for callables
"""

import warnings
from functools import partial, reduce, wraps
from inspect import Parameter, getmodule, signature
from logging import getLogger
from typing import Callable, Iterable, Type, TypeVar


def fullname(func: Callable) -> str:
    """
    Get full name of a function: the module it is declared in and it's name
    """
    module = getmodule(func)
    if module is None:
        return func.__name__
    return ".".join((module.__name__, func.__name__))


T = TypeVar("T", bound=Callable)  # pylint: disable=invalid-name


def rename(new_name: str) -> Callable[[T], T]:
    """
    Set a new name for a function
    """

    def decorator(func: T) -> T:
        func.__name__ = new_name
        return func

    return decorator


def identity(arg: T) -> T:
    """
    This function returns the first argument it receives.
    """
    return arg


def deprecated(func: T) -> T:
    """
    Warn when using wrapped func
    """
    func_name = fullname(func)

    @wraps(func)
    def decorated(*args, **kwargs):
        warnings.warn(f"{func_name} is deprecated", DeprecationWarning)
        return func(*args, **kwargs)

    return decorated  # type: ignore


def curry(_callable: Callable):
    """
    Creates a function that accepts arguments of func and either invokes func returning its result,
    if at least arity number of arguments have been provided, or returns a function that accepts
    the remaining func arguments, and so on.
    """

    _signature = signature(_callable)
    required_params = set()

    for name, parameter in _signature.parameters.items():
        if parameter.kind is Parameter.VAR_POSITIONAL:
            raise TypeError(
                "Curry can not be applied on a function with var positional parameters (*args)"
            )
        if (
            parameter.kind is not Parameter.VAR_KEYWORD
            and parameter.default is Parameter.empty
        ):
            required_params.add(name)

    @wraps(_callable)
    def curried(*args, **kwargs):
        bound = _signature.bind_partial(*args, **kwargs)
        if required_params - set(bound.arguments.keys()):
            return partial(curried, *args, **kwargs)
        return _callable(*args, **kwargs)

    return curried


O = TypeVar("O", bound=object)  # pylint: disable=invalid-name


class currymethod:  # pylint: disable=too-few-public-methods,invalid-name
    """
    Like curry but if the method was executed as a static method it will accept self as the last
    argument.
    """

    def __init__(self, method: Callable) -> None:
        self.method = curry(method)

        _signature = signature(method)

        # Should have used find() but it's a loop dependency
        self_param: Parameter
        for parameter in _signature.parameters.values():
            if parameter.kind in {
                Parameter.POSITIONAL_ONLY,
                Parameter.POSITIONAL_OR_KEYWORD,
            }:
                self_param = parameter
                break

        required_params = set()

        for name, parameter in _signature.parameters.items():
            if parameter.kind is Parameter.VAR_POSITIONAL:
                raise TypeError(
                    "Curry can not be applied on a function with var positional parameters (*args)"
                )
            if (
                parameter.kind is not Parameter.VAR_KEYWORD
                and parameter.default is Parameter.empty
            ):
                required_params.add(name)

        @wraps(method)
        def static(*args, **kwargs):
            bound = _signature.bind_partial(*args, **kwargs)
            if required_params - set(bound.arguments.keys()):
                return partial(static, *args, **kwargs)
            if self_param.name in kwargs:
                return method(*args, **kwargs)
            return method(args[-1], *args[0:-1], **kwargs)

        self.static = static

    def __get__(self, obj=None, objtype=None):
        if obj:
            return self.method(obj)
        return self.static


@curry
def flow(funcs: Iterable[Callable], value):
    """
    Creates a function that returns the result of invoking the given functions where each
    successive invocation is supplied the return value of the previous.
    """
    return reduce(lambda acc, func: func(acc), funcs, value)


def noop(*_, **__) -> None:
    """
    This method returns None
    """
    return None


Value = TypeVar("Value")


def constant(value: Value) -> Callable[..., Value]:
    """
    Creates a function that returns value.
    """

    def constant_func(*_, **__):
        return value

    return constant_func


def graceful(func: T, exception_type: Type[Exception] = Exception) -> T:
    """
    Creates a functions that returns the result of invoking the given function or None if
    it raised an exception.
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exception_type as exception:  # pylint: disable=broad-except
            getLogger().error(
                f"An exception has been raised while executing {func.__name__}: "
                + repr(exception)
            )
            return None

    return wrapped  # type: ignore
