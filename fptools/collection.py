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
    return reduce(lambda acc, item: operator.getitem(acc, item) if acc is not None else None, path, collection)

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
            sub = {}
        clone[key] = setitem(path[1:], value, sub)
            
    return clone

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
