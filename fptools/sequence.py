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
    return sequence[-1] if sequence else None
