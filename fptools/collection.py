import operator
from collections import Iterable, Hashable
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

def _mutable_setitem(path, value, collection):
    key = path[0]
    if len(path) == 1:
        collection[key] = value
    else:
        try:
            sub = collection[key]
        except KeyError:
            if isinstance(path[1], int):
                sub = [None] * (path[1] + 1)
            else:
                sub = {}
        collection[key] = setitem(path[1:], value, sub)
            
    return collection

@curry
def setitem(path, value, collection):
    '''
    Sets the value at path of collection. If a portion of path doesn't exist, it's created.
    '''
    path = to_path(path)
    clone = copy(collection)
    return _mutable_setitem(path, value, clone)


def _mutable_delitem(path, collection):
    item = path[0]
    if len(path) == 1:
        del collection[item]
    else:
        collection[item] = _mutable_delitem(path[1:], collection[item])
    return collection


@curry
def delitem(path, collection):
    path = to_path(path)
    clone = copy(collection)
    return _mutable_delitem(path, clone)


@curry
def update(path, modifier, collection):
    '''
    This method is like setitem except that it accepts an updater to produce the value to be set.
    '''
    value = getitem(path, collection)
    return setitem(path, modifier(value), collection)


@curry
def pick(paths, collection):
    paths = map(to_path, paths)
    clone = type(collection)()
    for path in paths:
        _mutable_setitem(path, getitem(path, collection), clone)
    return clone


@curry
def omit(paths, collection):
    paths = map(to_path, paths)
    clone = copy(collection)
    for path in paths:
        _mutable_delitem(path, clone)
    return clone
