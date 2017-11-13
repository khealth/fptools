from inspect import signature, Parameter, getargspec, isclass
from functools import reduce, partial, wraps
from logging import getLogger

def rename(newname):
    def decorator(f):
        f.__name__ = newname
        return f
    return decorator


_RESTRICTED_PARAMETER_KINDS = (
    Parameter.VAR_POSITIONAL, Parameter.KEYWORD_ONLY, Parameter.VAR_KEYWORD)

_CLASS_DEFAULT_PROPERTIES = (
    '__module__', '__init__', '__dict__', '__weakref__', '__doc__')

def _apply_self_last(method):
    self_arg = getargspec(method)[0][0]
    @wraps(method)
    def wrap(*args, **kwargs):
        if kwargs.get(self_arg):
            return method(*args, **kwargs)
        self = args[-1]
        return method(self, *args[0:-1], **kwargs)
    return wrap

def curry(_callable):
    '''
    Creates a function that accepts arguments of func and either invokes func returning its result,
    if at least arity number of arguments have been provided, or returns a function that accepts
    the remaining func arguments, and so on.
    '''

    if isclass(_callable):
        @rename(_callable.__name__)
        class curried(_callable):
            def __new__(self, *args, **kwargs):
                return _callable(*args, **kwargs)

            def __init__():
                pass

        for key, value in _callable.__dict__.items():
            if key in _CLASS_DEFAULT_PROPERTIES:
                continue
            if isinstance(value, classmethod):
                setattr(curried, key, curry(getattr(_callable, key)))
            if callable(value):
                setattr(curried, key, curry(_apply_self_last(value)))

        return curried

    parameters = signature(_callable).parameters
    for parameter in parameters.values():
        if parameter.kind in _RESTRICTED_PARAMETER_KINDS:
            raise NotImplementedError(
                'Curry can only be applied on functions with preknown number of parameters')
        if parameter.default is not Parameter.empty:
            raise NotImplementedError(
                'Curry can only be applied on functions with defaultless parameters')

    @wraps(_callable)
    def x(*args, **kwargs):
        if len(args) + len(kwargs) is len(parameters):
            return _callable(*args, **kwargs)
        return partial(x, *args, **kwargs)
    return x


@curry
def flow(funcs, value):
    '''
    Creates a function that returns the result of invoking the given functions where each
    successive invocation is supplied the return value of the previous.
    '''
    return reduce(lambda acc, func: func(acc), funcs, value)


def noop(*args, **kwargs):
    '''
    This method returns None
    '''
    return None


def constant(value):
    '''
    Creates a function that returns value.
    '''
    def constant_func(*args, **kwargs):
        return value
    return constant_func

def graceful(func):
    '''
    Creates a functions that returns the result of invoking the given function or None if
    it raised an exception.
    '''
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            getLogger().error(f'An error has been raised while executing {func.__name__}', e)
            return None
    return wrapped
