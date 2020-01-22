"""
Utilities for iterables
"""

from collections import abc
from dataclasses import dataclass
from functools import reduce
from itertools import tee
from operator import add
from typing import (
    Callable,
    Dict,
    Hashable,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)

from cardinality import count

from .callable import curry

T = TypeVar("T")  # pylint: disable=invalid-name


def compact(iterable: Iterable[T]) -> Iterable[T]:
    """
    Creates an iterable with all falsey values removed.
    """
    return filter(None, iterable)


def head(iterable: Iterable[T]) -> Optional[T]:
    """
    Gets the first element of iterable.
    Defaults to None.
    """
    try:
        return next(iter(iterable))
    except StopIteration:
        return None


@curry
def find(comparator: Callable[[T], bool], iterable: Iterable[T]) -> Optional[T]:
    """
    Iterates over elements of iterable, returning the first element predicate returns truthy for.
    Defaults to None.
    """
    for item in iterable:
        if comparator(item):
            return item
    return None


@curry
def find_index(comparator: Callable[[T], bool], iterable: Iterable[T]) -> Optional[int]:
    """
    This method is like find() except that it returns the index of the first element predicate
    returns truthy for instead of the element itself.
    """
    index = 0
    for item in iterable:
        if comparator(item):
            return index
        index += 1
    return None


Number = TypeVar("Number", bound=Union[int, float])


def mean(iterable: Iterable[Number]) -> float:
    """
    Computes the mean of the values in iterable.
    """
    to_sum, to_count = tee(iterable)
    _sum = reduce(add, to_sum)
    return _sum / count(to_count)


def flatten(iterable: Iterable[Union[T, Iterable[T]]]) -> Iterable[T]:
    """
    Flattens iterable a single level deep.
    """
    for item in iterable:
        if isinstance(item, abc.Iterable):
            yield from flatten(item)
        else:
            yield item


G = TypeVar("G")  # pylint: disable=invalid-name


@curry
def group_by(iteratee: Callable[[T], G], iterable: Iterable[T]) -> Dict[G, List[T]]:
    """
    Creates a dict composed of keys generated from the results of running each
    element of iterable thru iteratee. The order of grouped values is determined
    by the order they occur in iterable. The corresponding value of each key is
    a list of elements responsible for generating the key. The iteratee is
    invoked with one argument: (value).
    """
    groups: Dict[G, List[T]] = {}

    for item in iterable:
        key = iteratee(item)

        if not key:
            continue

        group = groups.setdefault(key, [])
        group.append(item)

    return groups


@dataclass
class FlatGroupBy(Iterable[Tuple[G, T]]):
    """
    The iterable object returned by flat_group_by()
    """

    iteratee: Callable[[T], G]
    iterable: Iterable[T]

    def __iter__(self):
        return (
            (group, item)
            for group, items in group_by(self.iteratee, self.iterable).items()
            for item in items
        )

    def __repr__(self) -> str:
        return f"flat_group_by({self.iteratee}, {self.iterable})"


@curry
def flat_group_by(
    iteratee: Callable[[T], G], iterable: Iterable[T]
) -> Iterable[Tuple[G, T]]:
    """
    Creates an iterable of tuples of group and item generated from the results
    of running each element of iterable thru iteratee. The order of grouped
    values is determined by the order they occur in iterable. The iteratee is
    invoked with one argument: (value). Like group_by but returns an iterable of
    tuples of group and item. Resembles SQL's group_by().
    """
    return FlatGroupBy(iteratee, iterable)


def key_by(iteratee: Callable[[T], G], iterable: Iterable[T]) -> Dict[G, T]:
    """
    Creates a dictionary composed of keys generated from the results of running
    each element of iterable thru iteratee. The corresponding value of each key
    is the last element responsible for generating the key. The iteratee is
    invoked with one argument: (value).
    """
    keyed = {}

    for item in iterable:
        key = iteratee(item)
        if key is None:
            continue
        keyed[key] = item

    return keyed


def _get_repeating(iterable):
    visited = set()
    for item in iterable:
        if item in visited:
            yield item
        else:
            visited = {*visited, item}


HashableItem = TypeVar("HashableItem", bound=Hashable)


@curry
def intersection(
    source: Iterable[HashableItem], target: Iterable[HashableItem]
) -> Iterable[HashableItem]:
    """
    Creates an iterable of unique values that are included in given source and
    target iterables using hash() for comparisons. The order and references of
    result values are determined by the first iterable.
    """
    return _get_repeating((*source, *target))


Identity = TypeVar("Identity")


@curry
def chunk_by(
    predicate: Callable[[T, int], Identity], iterable: Iterable[T]
) -> Iterable[Tuple[T, ...]]:
    """
    Creates an iterable of chunks of iterable defined by the identity returned
    by given predicate function
    """
    last_identity = None
    current_chunk: Tuple[T, ...] = tuple()
    for index, item in enumerate(iterable):
        identity = predicate(item, index)
        if identity is last_identity:
            current_chunk = current_chunk + (item,)
        else:
            if current_chunk:
                yield current_chunk
            last_identity = identity
            current_chunk = (item,)
    if current_chunk:
        yield current_chunk


@curry
def chunk(size: int, iterable: Iterable[T]) -> Iterable[Tuple[T, ...]]:
    """
    Creates an iterable of elements split into groups the length of size.
    If iterable can't be split evenly, the final chunk will be the remaining elements.
    """
    return chunk_by(lambda item, index: index // size, iterable)


def uniq(iterable: Iterable[T]) -> Iterable[T]:
    """
    Returns a duplicate-free version of an iterable, using hash for equality
    comparisons, in which only the first occurrence of each element is kept.
    The order of result values is determined by the order they occur in the
    iterable.
    """
    seen: Set[T] = set()
    for item in iterable:
        if item in seen:
            continue
        seen.add(item)
        yield item


Key = TypeVar("Key", bound=Hashable)


def uniq_by(key: Callable[[T], Key], iterable: Iterable[T]) -> Iterable[T]:
    """
    This function is like uniq except that it accepts iteratee which is invoked
    for each element in array to generate the criterion by which uniqueness is
    computed. The order of result values is determined by the order they occur
    in the array. The iteratee is invoked with one argument: (value).
    """
    seen: Set[Key] = set()
    for item in iterable:
        k = key(item)
        if k in seen:
            continue
        seen.add(k)
        yield item


def index_of(item: T, iterable: Iterable[T]) -> Optional[int]:
    """
    Returns index of item in given iterable. Like list.index() but for any iterable
    """
    for index, _item in enumerate(iterable):
        if _item == item:
            return index
    return None


A = TypeVar("A") # pylint: disable=invalid-name


def starreduce(function: Callable[[A, T], A], iterable: Iterable[Iterable[T]], initial: A) -> A:
    """
    Make an iterator that computes the function using arguments obtained from
    the iterable. Used instead of reduce() when argument parameters are already
    grouped in tuples from a single iterable (the data has been “pre-zipped”).
    The difference between reduce() and starreduce() parallels the distinction
    between function(a,b) and function(*c)
    """
    return reduce(lambda acc, item: function(acc, *item), iterable, initial)


def starfilter(function: Callable[[T], bool], iterable: Iterable[Iterable[T]]) -> Iterable[T]:
    """
    Make an iterator that computes the function using arguments obtained from
    the iterable. Used instead of filter() when argument parameters are already
    grouped in tuples from a single iterable (the data has been “pre-zipped”).
    The difference between filter() and starfilter() parallels the distinction
    between function(a,b) and function(*c)
    """
    return filter(lambda item: function(*item), iterable) # type: ignore


def partition(predicate: Callable[[T], bool], iterable: Iterable[T]) -> Tuple[Iterable[T], Iterable[T]]:
    """
    Partition given iterable items to two iterables: of items matching the
    predicate function and items that do not.
    """
    matching: List[T] = []
    non_matching: List[T] = []
    for item in iterable:
        if predicate(item):
            matching.append(item)
        else:
            non_matching.append(item)
    return matching, non_matching
            