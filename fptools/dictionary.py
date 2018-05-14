from collections import Iterable, Hashable
from functools import reduce
from .callable import curry
from .collection import getitem, pick


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


def extract(*keys, **aliases):
    def extractor(_dict):
        return {
            **{ key: getitem(value, _dict) for key, value in aliases.items() },
            **pick(keys, _dict)
        }
    return extractor


@curry
def map_values(modifier, _dict):
    '''
    Creates a dictionary with the same keys as _dict and values generated by applying modifier(val) for each value.
    '''
    return {key: modifier(value) for key, value in _dict.items()}

@curry
def map_keys(modifier, _dict):
    '''
    Creates a dictionary with the same values as _dict and keys generated by applying modifier(key) for each key.
    '''
    return {modifier(key): value for key, value in _dict.items()}


@curry
def apply_spec(spec, _dict):
    return {**_dict, 
            **{key: func(_dict[key]) 
               for key, func in spec.items()}}

def is_dict(value):
    '''
    Matches if value is a dictionary
    '''
    return isinstance(value, dict)


def branches(_dict):
    '''
    Iterates each keys and value pair of the dictionary and it's descendent dicts
    '''
    for key, value in _dict.items():
        yield (key,), value
        if isinstance(value, dict):
            for path, subvalue in branches(value):
                yield (key,) + path, subvalue

def leaves(_dict):
    '''
    Like iterate_branches() but only yields non dict values
    '''
    for keys, value in branches(_dict):
        if not isinstance(value, dict):
            yield keys, value
