"""
Utilities for working with Optional[T]
"""


from typing import TypeVar, Callable, Iterable, Optional
from functools import wraps


T = TypeVar('T')
T2 = TypeVar('T2')


def ignore_optional(func: Callable[[T], T2]):
    """
    Returns a new function only applied for non None value
    """
    @wraps(func)
    def wrap(item: Optional[T]) -> Optional[T2]:
        return func(item) if item is not None else None
    return wrap


def map_optionals(iteratee: Callable[[T], T2], iterable: Iterable[Optional[T]]) -> Iterable[Optional[T2]]:
    """
    Maps items of iterable with iteratee without affecting None items.
    """
    return map(ignore_optional(iteratee), iterable)


def is_some(value: Optional[T]) -> bool:
    """
    Returns whether a value is not None
    """
    return value is not None
