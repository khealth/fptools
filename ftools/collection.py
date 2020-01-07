"""
Utilities for collection
"""

# A collection in this context is Mapping or Iterable that is not a str

import operator
from collections import abc
from copy import copy
from typing import (
    TypeVar,
    Union,
    Iterable as IterableT,
    Callable,
    MutableSequence,
    Mapping,
    MutableMapping,
    Generator,
    Tuple,
    Hashable,
    Sequence,
)
from cardinality import count
from .callable import curry
from .iterable import head
from .sequence import pick as sequence_pick
from .mapping import pick as mapping_pick

# This is actually Mapping x Iterable / str
Item = Union[Hashable, int]
K = TypeVar("K")  # pylint: disable=invalid-name
V = TypeVar("V")  # pylint: disable=invalid-name
Collection = Union[
    Mapping[Item, Union["Collection", V]], IterableT[Union["Collection", V]]
]
MutableCollection = Union[
    MutableMapping[K, Union["MutableCollection", V]],
    MutableSequence[Union["MutableCollection", V]],
]

RawPath = Union[Item, Sequence[Item]]
Path = Sequence[Item]


def to_path(path: RawPath) -> Path:
    """
    Converts value to a property path tuple.
    """
    if isinstance(path, abc.Iterable):
        if isinstance(path, str):
            return (path,)
        return path
    return (path,)


@curry
def getitem(path: RawPath, collection: Collection) -> V:
    """
    Gets the value at path of collection
    """
    path = to_path(path)
    value = collection
    for key in path:
        try:
            value = operator.getitem(value, key)
        except (KeyError, TypeError, IndexError):
            return None
    return value


@curry
def hasitem(path: RawPath, collection: Collection) -> bool:
    """
    Returns whether path exists in collection
    """
    path = to_path(path)
    value = collection
    for key in path:
        try:
            value = operator.getitem(value, key)
        except (KeyError, TypeError, IndexError):
            return False
    return True


def _safe_setitem(item, value, collection):
    try:
        collection[item] = value
    except IndexError:
        for i in range(len(collection), item + 1):
            collection.insert(i, None)
        collection[item] = value


@curry
def setitem(
    path: RawPath, value: V, collection: MutableCollection
) -> MutableCollection:
    """
    Sets the value at path of collection. If a portion of path doesn't exist, it's created.
    """
    path = to_path(path)
    clone = copy(collection)
    key = head(path)
    if count(path) == 1:
        _safe_setitem(key, value, clone)
    else:
        try:
            sub = collection[key]
        except KeyError:
            if isinstance(path[1], int):
                sub = []
            else:
                sub = {}
        except IndexError:
            for i in range(len(clone), key + 1):
                clone.insert(i, None)
            if isinstance(path[1], int):
                sub = []
            else:
                sub = {}
        clone[key] = setitem(path[1:], value, sub)

    return clone


@curry
def delitem(path: RawPath, collection: MutableCollection) -> MutableCollection:
    """
    Deletes given path from collection
    """
    path = to_path(path)
    clone = copy(collection)
    key = head(path)
    if count(path) == 1:
        del clone[key]
    else:
        clone[key] = delitem(path[1:], collection[key])
    return clone


@curry
def update(
    path: RawPath, modifier: Callable[[V], V], collection: MutableCollection
) -> MutableCollection:
    """
    This method is like set except that accepts updater to produce the value to set.
    """
    value = getitem(path, collection)
    return setitem(path, modifier(value), collection)


def branches(
    collection: Collection,
) -> Generator[Tuple[Path, Union[Collection, V]], None, None]:
    """
    Iterates each path and value pair of the collection and it's descendent collections
    """
    from .mapping import items  # pylint: disable=import-outside-toplevel

    if isinstance(collection, abc.Mapping):
        iterator = items(collection)
    elif isinstance(collection, abc.Iterable):
        iterator = enumerate(collection)

    for key, value in iterator:
        yield (key,), value
        if isinstance(value, (abc.Mapping, abc.Iterable)) and not isinstance(
            value, str
        ):
            for path, subvalue in branches(value):
                yield (key,) + path, subvalue


def leaves(collection: Collection) -> Generator[Tuple[Path, V], None, None]:
    """
    Like branches() but only yields non collection values
    """
    for keys, value in branches(collection):
        if not isinstance(value, (abc.Mapping, abc.Iterable)) or isinstance(value, str):
            yield keys, value


def _pick(path_tree, collection):
    items = path_tree.keys()
    if isinstance(collection, abc.Sequence):
        next_collection = sequence_pick(items, collection)
        for i, item in enumerate(sorted(items)):
            if isinstance(path_tree[item], dict):
                next_collection[i] = _pick(path_tree[item], next_collection[i])
    elif isinstance(collection, abc.Mapping):
        next_collection = mapping_pick(items, collection)
        for item in items:
            if isinstance(path_tree[item], dict):
                next_collection[item] = _pick(path_tree[item], next_collection[item])
    else:
        raise NotImplementedError
    return next_collection


def _create_path_tree(paths):
    tree = {}
    for path in paths:
        cursor = tree
        path = to_path(path)
        for item in path[:-1]:
            if item not in cursor:
                cursor[item] = {}
            cursor = cursor[item]
        cursor[path[-1]] = True
    return tree


def pick(paths: IterableT[RawPath], collection: Collection) -> Collection:
    """
    Creates a collection composed of the picked paths.
    """
    path_tree = _create_path_tree(paths)
    return _pick(path_tree, collection)
