from fptools.mapping import create_empty, pick, omit, map_keys, map_values, is_dict, items, extract


def test_create_empty():
    assert create_empty({ "a": 1 }) == {}
    assert create_empty({}) == {}


def test_extract():
    base = {"a": 1, "b": 2}
    res = extract("a", c="b")(base)
    assert res == {"a": 1, "c": 2}


def test_pick():
    assert pick({'foo', 'bar'}, {'foo': 4, 'bar': 2, 'yo': 3}) == {
        'foo': 4, 'bar': 2}


def test_omit():
    assert omit({'foo', 'bar', 'non_existing'}, {'foo': 4, 'bar': 2, 'yo': 3}) == {'yo': 3}


def test_map_values():
    assert map_values(lambda value: value * 2,
                      {'a': 1, 'b': 2}) == {'a': 2, 'b': 4}


def test_map_keys():
    assert map_keys(lambda value: value * 2,
                    {'a': 1, 'b': 2}) == {'aa': 1, 'bb': 2}


def test_is_dict():
    assert is_dict(4) == False
    assert is_dict({}) == True


def test_items():
    _items = items({'a': 1, 'b': 2, 'c': 3})
    assert list(_items) == [
        ('a', 1),
        ('b', 2),
        ('c', 3)
    ]
    assert ("a" in _items) is True