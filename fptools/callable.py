import warnings
from typing import Callable, TypeVar, Union, Any, Iterable
from inspect import signature, Parameter
from functools import reduce, partial, wraps
from inspect import getmodule
from logging import getLogger


def fullname(func : Callable) -> str:
    '''
    Get full name of a function: the module it is declared in and it's name
    '''
    return '.'.join((getmodule(func).__name__, func.__name__))


def rename(newname : str) -> Callable[[Callable], Callable]:
    '''
    Set a new name for a function
    '''
    def decorator(f : Callable) -> Callable:
        f.__name__ = newname
        return f
    return decorator


T = TypeVar('T')


def identity(arg : T) -> T:
    '''
    This function returns the first argument it receives.
    '''
    return arg


def deprecated(func : Callable) -> Callable:
    '''
    Warn when using wrapped func
    '''
    func_name = fullname(func)

    @wraps(func)
    def decorated(*args, **kwargs):
        warnings.warn(f'{func_name} is deprecated', DeprecationWarning)
        return func(*args, **kwargs)

    return decorated


_RESTRICTED_PARAMETER_KINDS = (
    Parameter.VAR_POSITIONAL, Parameter.KEYWORD_ONLY, Parameter.VAR_KEYWORD)


R = TypeVar('R')


def curry(_callable: Callable[..., R]) -> Union[R, Callable[..., Any]]:
    '''
    Creates a function that accepts arguments of func and either invokes func returning its result,
    if at least arity number of arguments have been provided, or returns a function that accepts
    the remaining func arguments, and so on.
    '''

    parameters = signature(_callable).parameters.values()
    defaultless_parameters_len = len(
        [p for p in parameters if p.default is Parameter.empty])
    optionals_names = {
        p.name for p in parameters if p.default is not Parameter.empty}
    for parameter in parameters:
        if parameter.kind in _RESTRICTED_PARAMETER_KINDS:
            raise NotImplementedError(
                'Curry can only be applied on functions with preknown number of parameters')

    @wraps(_callable)
    def x(*args, **kwargs):
        non_optional_kwargs_len = len(
            [k for k in kwargs if k not in optionals_names])
        if len(args) + non_optional_kwargs_len >= defaultless_parameters_len:
            return _callable(*args, **kwargs)
        return partial(x, *args, **kwargs)
    return x


_RESTRICTED_PARAMETER_KINDS = (
    Parameter.VAR_POSITIONAL, Parameter.KEYWORD_ONLY, Parameter.VAR_KEYWORD)


class currymethod:
    '''
    Like curry but if the method was executed as a static method it will accept self as the last
    argument.
    '''

    def __init__(self, method):
        self.method = curry(method)

        parameters = signature(method).parameters.values()
        defaultless_parameters_len = len(
            [p for p in parameters if p.default is Parameter.empty])
        optionals_names = {
            p.name for p in parameters if p.default is not Parameter.empty}
        for parameter in parameters:
            if parameter.kind in _RESTRICTED_PARAMETER_KINDS:
                raise NotImplementedError(
                    'Curry can only be applied on functions with preknown number of parameters')

        @wraps(method)
        def x(*args, **kwargs):
            non_optional_kwargs_len = len(
                [k for k in kwargs if k not in optionals_names])
            if len(args) + non_optional_kwargs_len >= defaultless_parameters_len:
                return method(args[-1], *args[0:-1], **kwargs)
            return partial(x, *args, **kwargs)
        self.static = x

    def __get__(self, obj=None, objtype=None):
        if obj:
            return self.method(obj)
        return self.static


@curry
def flow(funcs : Iterable[Callable], value):
    '''
    Creates a function that returns the result of invoking the given functions where each
    successive invocation is supplied the return value of the previous.
    '''
    return reduce(lambda acc, func: func(acc), funcs, value)


def noop(*args, **kwargs) -> None:
    '''
    This method returns None
    '''
    return None


def constant(value : T) -> Callable[..., T]:
    '''
    Creates a function that returns value.
    '''
    def constant_func(*args, **kwargs):
        return value
    return constant_func


def graceful(func : Callable) -> Callable:
    '''
    Creates a functions that returns the result of invoking the given function or None if
    it raised an exception.
    '''
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            getLogger().error(
                f'An error has been raised while executing {func.__name__}', e)
            return None
    return wrapped
