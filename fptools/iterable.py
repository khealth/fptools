from functools import reduce
from collections import Iterable
from operator import add
from fptools.callable import curry
from fptools.dictionary import update


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


def avg(iterable):
    return reduce(add, iterable) / len(iterable)


def flatten(iterable):
    return reduce(lambda acc, item: acc + (flatten(item) if isinstance(item, Iterable) else [item]), iterable, [])

@curry
def group_by(predicate, iterable):
    def accumulate(groups, item):
        key = predicate(item)
        if not key:
            return groups
        return update(key, lambda group: (group or []) + [item], groups)
    return reduce(accumulate, iterable, {})

def _get_repeating(iterable):
    visited = set()
    for item in iterable:
        if item in visited:
            yield item
        else:
            visited = { *visited, item }

@curry
def intersection(source, target):
    return tuple(_get_repeating((*source, *target)))
