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


def avg(_list):
    return reduce(add, _list) / len(_list)


def flatten(_list):
    return reduce(lambda acc, item: acc + (flatten(item) if isinstance(item, Iterable) else [item]), _list, [])


@curry
def group_by(predicate, iterable):
    return reduce(lambda groups, item: update(predicate(item), lambda group: (group or []) + [item], groups), iterable, {})
