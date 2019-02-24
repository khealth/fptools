from fptools.mapping import pick, omit, map_values, is_dict, items


def test_pick():
    assert pick({'foo', 'bar'}, {'foo': 4, 'bar': 2, 'yo': 3}) == {
        'foo': 4, 'bar': 2}


def test_omit():
    assert omit({'foo', 'bar'}, {'foo': 4, 'bar': 2, 'yo': 3}) == {'yo': 3}


def test_map_values():
    assert map_values(lambda value: value * 2,
                      {'a': 1, 'b': 2}) == {'a': 2, 'b': 4}


def is_dict():
    assert is_dict(4) == False
    assert is_dict({}) == True


def test_items():
    assert list(items({'a': 1, 'b': 2, 'c': 3})) == [
        ('a', 1),
        ('b', 2),
        ('c', 3)
    ]
