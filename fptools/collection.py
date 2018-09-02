# A collection in this context is Mapping or Iterable that is not a str

import operator
from collections import Mapping, Iterable, Hashable
from copy import copy
from functools import reduce
from typing import Any, TypeVar, Union, Iterable as IterableT, Callable, MutableSequence, Mapping, MutableMapping, Generator, Tuple
from cardinality import count
from fptools.callable import curry
from fptools.iterable import head

# This is actually Mapping x Iterable / str
K = TypeVar('K')
V = TypeVar('V')
Collection = Union[Mapping[K, Union['Collection', V]],
                   IterableT[Union['Collection', V]]]
MutableCollection = Union[MutableMapping[K, Union['MutableCollection', V]],
                          MutableSequence[Union['MutableCollection', V]]]

# TODO define more generic item
ItemKey = Union[str, int]
RawPath = Union[ItemKey, IterableT[ItemKey]]
Path = IterableT[ItemKey]


def to_path(path: RawPath) -> Path:
    '''
    Converts value to a property path tuple.
    '''
    if isinstance(path, Iterable):
        if isinstance(path, str):
            return (path,)
        return path
    return (path,)


@curry
def getitem(path: RawPath, collection: Collection) -> V:
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
def setitem(path: RawPath, value: V, collection: MutableCollection) -> MutableCollection:
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
def delitem(path: RawPath, collection: MutableCollection) -> MutableCollection:
    path = to_path(path)
    clone = copy(collection)
    key = head(path)
    if count(path) == 1:
        del clone[key]
    else:
        clone[key] = delitem(path[1:], collection[key])
    return clone


@curry
def update(path: RawPath, modifier: Callable[[V], V], collection: MutableCollection) -> MutableCollection:
    '''
    This method is like set except that accepts updater to produce the value to set.
    '''
    value = getitem(path, collection)
    return setitem(path, modifier(value), collection)


from fptools.dictionary import items


def branches(collection: Collection) -> Generator[Tuple[Path, Union[Collection, V]], None, None]:
    '''
    Iterates each path and value pair of the collection and it's descendent collections
    '''
    if isinstance(collection, Mapping):
        iterator = items(collection)
    elif isinstance(collection, Iterable):
        iterator = enumerate(collection)

    for key, value in iterator:
        yield (key, ), value
        if isinstance(value,
                      (Mapping, Iterable)) and not isinstance(value, str):
            for path, subvalue in branches(value):
                yield (key, ) + path, subvalue


def leaves(collection: Collection) -> Generator[Tuple[Path, V], None, None]:
    '''
    Like branches() but only yields non collection values
    '''
    for keys, value in branches(collection):
        if not isinstance(value,
                          (Mapping, Iterable)) or isinstance(value, str):
            yield keys, value
