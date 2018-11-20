from functools import reduce
from itertools import tee
from collections import Iterable
from operator import add
from cardinality import count
from .callable import curry


def compact(iterable):
    return filter(None, iterable)


def head(iterable):
    try:
        return next(iter(iterable))
    except StopIteration:
        return None


@curry
def find(comparator, iterable):
    for item in iterable:
        if comparator(item):
            return item
    return None


@curry
def find_index(comparator, iterable):
    index = 0
    for item in iterable:
        if comparator(item):
            return index
        index += 1
    return None


def mean(iterable):
    to_sum, to_count = tee(iterable)
    return reduce(add, to_sum) / count(to_count)


def flatten(iterable):
    for item in iterable:
        if isinstance(item, Iterable):
            yield from flatten(item)
        else:
            yield item


@curry
def group_by(predicate, iterable):
    groups = {}

    for item in iterable:
        key = predicate(item)

        if not key:
            continue

        group = groups.setdefault(key, [])
        group.append(item)

    return groups


def key_by(iteratee, iterable):
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
    Creates a list of elements split into groups the length of size. If list can't be split evenly, the final chunk will be the remaining elements.
    '''
    return chunk_by(lambda item, index: index // size, iterable)
