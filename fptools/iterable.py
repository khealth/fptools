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


def group_by(predicate, iterable):
    return reduce(lambda groups, item: update(predicate(item), lambda group: (group or []) + [item], groups), iterable, {})

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
