from fptools.dictionary import map_values, is_dict, branches, leaves


def test_map_values():
    assert map_values(lambda value: value * 2,
                      {'a': 1, 'b': 2}) == {'a': 2, 'b': 4}


def test_is_dict():
    assert is_dict(4) == False
    assert is_dict({}) == True


def test_branches():
    assert list(branches({ 'a': 1 })) == [(('a',), 1)]
    assert list(branches({ 'a': { 'b': { 'c': 1 } } })) == [
        (('a',), { 'b': { 'c': 1 }}),
        (('a', 'b',), { 'c': 1 }),
        (('a', 'b', 'c'), 1),
    ]

def test_leaves():
    assert list(leaves({ 'a': 1 })) == [(('a',), 1)]
    assert list(leaves({ 'a': { 'b': { 'c': 1 } } })) == [
        (('a', 'b', 'c'), 1),
    ]
