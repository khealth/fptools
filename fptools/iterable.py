from functools import reduce
from itertools import tee
from collections import Iterable
from operator import add
from cardinality import count
from .callable import curry


def compact(iterable):
    """
    Creates an iterable with all falsey values removed.
    """
    return filter(None, iterable)


def head(iterable):
    """
    Gets the first element of iterable.
    Defaults to None.
    """
    try:
        return next(iter(iterable))
    except StopIteration:
        return None


@curry
def find(comparator, iterable):
    """
    Iterates over elements of iterable, returning the first element predicate returns truthy for.
    Defaults to None.
    """
    for item in iterable:
        if comparator(item):
            return item
    return None


@curry
def find_index(comparator, iterable):
    """
    This method is like find() except that it returns the index of the first element predicate returns truthy for
    instead of the element itself.
    """
    index = 0
    for item in iterable:
        if comparator(item):
            return index
        index += 1
    return None


def mean(iterable):
    """
    Computes the mean of the values in iterable.
    """
    to_sum, to_count = tee(iterable)
    return reduce(add, to_sum) / count(to_count)


def flatten(iterable):
    """
    Flattens iterable a single level deep.
    """
    for item in iterable:
        if isinstance(item, Iterable):
            yield from flatten(item)
        else:
            yield item


@curry
def group_by(predicate, iterable):
    """
    Creates an iterable composed of keys generated from the results of running each element of iterable thru iteratee.
    The order of grouped values is determined by the order they occur in iterable. The corresponding value of each key
    is a list of elements responsible for generating the key. The iteratee is invoked with one argument: (value).
    """
    groups = {}

    for item in iterable:
        key = predicate(item)

        if not key:
            continue

        group = groups.setdefault(key, [])
        group.append(item)

    return groups


def key_by(iteratee, iterable):
    """
    Creates a dictionary composed of keys generated from the results of running each element of iterable thru iteratee.
    The corresponding value of each key is the last element responsible for generating the key. The iteratee is invoked
    with one argument: (value).
    """
    keyed = {}

    for item in iterable:
        key = iteratee(keyed)
        keyed[key] = item

    return keyed


def _get_repeating(iterable):
    visited = set()
    for item in iterable:
        if item in visited:
            yield item
        else:
            visited = {*visited, item}


@curry
def intersection(source, target):
    """
    Creates an iterable of unique values that are included in given source and target iterables using hash() for
    comparisons. The order and references of result values are determined by the first iterable.
    """
    return _get_repeating((*source, *target))


@curry
def chunk_by(predicate, iterable):
    last_identity = None
    current_chunk = tuple()
    for index, item in enumerate(iterable):
        identity = predicate(item, index)
        if identity is last_identity:
            current_chunk = current_chunk + (item, )
        else:
            if current_chunk:
                yield current_chunk
            last_identity = identity
            current_chunk = (item, )
    if current_chunk:
        yield current_chunk


@curry
def chunk(size, iterable):
    '''
    Creates an iterable of elements split into groups the length of size.
    If iterable can't be split evenly, the final chunk will be the remaining elements.
    '''
    return chunk_by(lambda item, index: index // size, iterable)
