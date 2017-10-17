from functools import reduce
from fptools.callable import curry


def initial(sequence):
    '''
    Gets all but the last element of sequence.
    '''
    return sequence[:-1]


def last(sequence):
    '''
    Gets the last element of sequence.
    '''
    return sequence[-1]


@curry
def chunk_by(predicate, sequence):
    last_identity = None

    def accumulate(acc, entry):
        nonlocal last_identity
        index, item = entry
        identity = predicate(item, index)
        if identity is last_identity:
            return initial(acc) + [last(acc) + [item]]
        else:
            last_identity = identity
            return acc + [[item]]

    return reduce(accumulate, enumerate(sequence), [])


@curry
def chunk(size, sequence):
    '''
    Creates a list of elements split into groups the length of size. If list can't be split evenly, the final chunk will be the remaining elements.
    '''
    return chunk_by(lambda item, index: index // size, sequence)
