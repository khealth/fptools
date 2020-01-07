"""
Utilities for sequences
"""

from typing import TypeVar, Sequence, MutableSequence, Iterable, Optional
from copy import copy

T = TypeVar("T")  # pylint: disable=invalid-name


def create_empty(sequence: MutableSequence[T]) -> MutableSequence[T]:
    """
    Create a new sequence of the type of given sequence
    """
    try:
        return type(sequence)()
    except TypeError:
        next_sequence = copy(sequence)
        next_sequence.clear()
        return next_sequence


def initial(sequence: Sequence[T]) -> Sequence[T]:
    """
    Gets all but the last element of sequence.
    """
    return sequence[:-1]


def last(sequence: Sequence[T]) -> Optional[T]:
    """
    Gets the last element of sequence.
    """
    return sequence[-1] if sequence else None


def pick(items: Iterable[int], sequence: MutableSequence[T]) -> MutableSequence[T]:
    """
    Creates a sequence composed of the picked sequence items.
    """
    next_sequence = create_empty(sequence)
    for item in items:
        try:
            next_sequence.append(sequence[item])
        except IndexError:
            pass
    return next_sequence


def omit(items: Iterable[int], sequence: MutableSequence[T]) -> MutableSequence[T]:
    """
    The opposite of pick; this method creates a sequence composed of the items that are not omitted.
    """
    next_sequence = copy(sequence)
    for item in sorted(items, reverse=True):
        try:
            del next_sequence[item]
        except IndexError:
            continue
    return next_sequence
