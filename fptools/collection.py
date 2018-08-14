import operator
from typing import Union, Optional
from collections.abc import Iterable, Hashable, MutableMapping, MutableSequence
from copy import copy
from functools import reduce
from fptools.callable import curry


def to_path(path):
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


@curry
def getitem(path, collection):
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
def setitem(path, value, collection):
    '''
    Sets the value at path of collection. If a portion of path doesn't exist, it's created.
    '''
    path = to_path(path)
    clone = copy(collection)
    key = path[0]
    if len(path) == 1:
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


def _get_new_collection_for_key(key):
    if isinstance(key, int):
        return []
    return {}


def mut_setitem(path, value, collection) -> None:
    '''
    Sets the value at path of collection. If a portion of path doesn't exist, it's created.
    This methods modifies the given collection
    '''
    parent: Optional[Union[MutableSequence, MutableMapping]] = None
    sub = collection
    *initial, last = to_path(path)
    for key_index, key in enumerate(initial):
        try:
            parent = sub
            sub = parent[key]
            if not isinstance(sub, (MutableMapping, MutableSequence)):
                next_key = path[key_index + 1]
                sub = _get_new_collection_for_key(next_key)
                parent[key] = sub
        except KeyError:
            next_key = path[key_index + 1]
            new_sub = _get_new_collection_for_key(next_key)
            sub[key] = new_sub
            parent = sub
            sub = parent[key]

    sub[last] = value


@curry
def delitem(path, collection):
    path = to_path(path)
    clone = copy(collection)
    key = path[0]
    if len(path) == 1:
        del clone[key]
    else:
        clone[key] = delitem(path[1:], collection[key])
    return clone


@curry
def update(path, modifier, collection):
    '''
    This method is like set except that accepts updater to produce the value to set.
    '''
    value = getitem(path, collection)
    return setitem(path, modifier(value), collection)
