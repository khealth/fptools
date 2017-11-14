import operator
from collections import Iterable, Hashable
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
def getitem(path, _dict):
    '''
    Gets the value at path of dictionary
    '''
    path = to_path(path)
    return reduce(lambda acc, item: operator.getitem(acc, item) if acc is not None else None, path, _dict)


@curry
def setitem(path, value, collection):
    '''
    Sets the value at path of dictionary. If a portion of path doesn't exist, it's created.
    '''
    path = to_path(path)
    clone = copy(collection)
    if len(path) > 1:
      clone[path[0]] = value
    else:
      clone[path[0]] = setitem(path[1:], value, collection[path[0]])
    return clone


@curry
def delitem(path, _dict):
    path = to_path(path)
    if len(path) > 1:
        return {
            **_dict,
            path[0]: delitem(path[1:], _dict.get(path[0]))
        }
    new_dict = {**_dict}
    del new_dict[path[0]]
    return new_dict


@curry
def update(path, modifier, _dict):
    '''
    This method is like set except that accepts updater to produce the value to set.
    '''
    value = getitem(path, _dict)
    return setitem(path, modifier(value), _dict)
