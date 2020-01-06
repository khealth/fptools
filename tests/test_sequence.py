from collections.abc import MutableSequence
from ftools.sequence import initial, last, pick, omit, create_empty


def test_initial():
    assert initial((1, 2, 3)) == (1, 2)


class NoInitMutableSequence(MutableSequence):
    """
    Test sequence is a sequence that can 
    """
    def __init__(self, *items):
        if len(items) == 0:
            raise TypeError
        self.items = list(items)

    def __getitem__(self, *args, **kwargs):
        return self.items.__getitem__(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        return self.items.__setitem__(*args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        return self.items.__delitem__(*args, **kwargs)

    def __len__(self):
        return self.items.__len__()

    def insert(self, *args, **kwargs):
        self.items.insert(*args, **kwargs)


def test_create_empty():
    assert create_empty([1, 2, 3]) == []
    empty = create_empty(NoInitMutableSequence(1, 2, 3))
    assert isinstance(empty, NoInitMutableSequence)
    assert len(empty) == 0


def test_last():
    assert last([]) is None
    assert last((1, 2)) is 2


def test_pick():
    assert pick({1, 2}, [1, 2, 3]) == [2, 3]
    assert pick({1, 2}, []) == []
    assert pick({1, 2}, [1, 2]) == [2]


def test_omit():
    assert omit({1, 2}, [1, 2, 3]) == [1]
    assert omit({1, 2}, []) == []
    assert omit({1, 2}, [1, 2]) == [1]
