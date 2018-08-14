import operator
from collections import Iterable, Hashable
from copy import copy
from functools import reduce
from typing import Any, TypeVar, Union, Iterable as IterableT, Callable, MutableSequence, MutableMapping
from cardinality import count
from fptools.callable import curry
from fptools.iterable import head

ItemKey = Union[str, int]
RawPath = Union[ItemKey, IterableT[ItemKey]]
Path = IterableT[ItemKey]


def to_path(path: RawPath) -> Path:
    '''
    Converts value to a property path tuple.
    '''
    if isinstance(path, Hashable) and not isinstance(path, tuple):
        return (path,)
    elif isinstance(path, Iterable):
        return path
    else:
        raise NotImplementedError(
            f'{path} is not a path. A path must be an iterable or a string not a {type(path)}')


Collection = TypeVar('Collection', MutableSequence, MutableMapping)


@curry
def getitem(path: RawPath, collection: Collection) -> Any:
    '''
    Gets the value at path of collection
    '''
    path = to_path(path)
    value = collection
    for key in path:
        try:
            value = operator.getitem(value, key)
        except (KeyError, TypeError, IndexError):
            return None
    return value


@curry
def hasitem(path: RawPath, collection: Collection) -> bool:
    path = to_path(path)
    value = collection
    for key in path:
        try:
            value = operator.getitem(value, key)
        except (KeyError, TypeError, IndexError):
            return False
    return True


@curry
def setitem(path: RawPath, value: Any, collection: Collection) -> Collection:
    '''
    Sets the value at path of collection. If a portion of path doesn't exist, it's created.
    '''
    path = to_path(path)
    clone = copy(collection)
    key = head(path)
    if count(path) == 1:
        clone[key] = value
    else:
        try:
            sub = collection[key]
        except KeyError:
            if isinstance(path[1], int):
                sub = [None] * (path[1] + 1)
            else:
                sub = {}
        clone[key] = setitem(path[1:], value, sub)

    return clone


@curry
def delitem(path: RawPath, collection: Collection) -> Collection:
    path = to_path(path)
    clone = copy(collection)
    key = head(path)
    if count(path) == 1:
        del clone[key]
    else:
        clone[key] = delitem(path[1:], collection[key])
    return clone


@curry
def update(path: RawPath, modifier: Callable, collection: Collection) -> Collection:
    '''
    This method is like set except that accepts updater to produce the value to set.
    '''
    value = getitem(path, collection)
    return setitem(path, modifier(value), collection)
