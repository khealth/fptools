from inspect import signature, Parameter
from functools import reduce, partial, wraps

RESTRICTED_PARAMETER_KINDS = (
    Parameter.VAR_POSITIONAL, Parameter.KEYWORD_ONLY, Parameter.VAR_KEYWORD)


def curry(func):
    '''
    Creates a function that accepts arguments of func and either invokes func returning its result,
    if at least arity number of arguments have been provided, or returns a function that accepts
    the remaining func arguments, and so on.
    '''
    parameters = signature(func).parameters
    for parameter in signature(func).parameters.values():
        if parameter.kind in RESTRICTED_PARAMETER_KINDS:
            raise NotImplementedError(
                'Curry can only be applied on functions with preknown number of parameters')
        if parameter.default is not Parameter.empty:
            raise NotImplementedError(
                'Curry can only be applied on functions with defaultless parameters')

    @wraps(func)
    def x(*args, **kwargs):
        if len(args) + len(kwargs) is len(parameters):
            return func(*args, **kwargs)
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
