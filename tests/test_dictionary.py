from fptools.dictionary import pick, omit, map_values, is_dict, map_keys_by_layer


def test_pick():
    assert pick(('foo', 'bar'), {'foo': 4, 'bar': 2, 'yo': 3}) == {
        'foo': 4, 'bar': 2}


def test_omit():
    assert omit(('foo', 'bar'), {'foo': 4, 'bar': 2, 'yo': 3}) == {'yo': 3}


def test_map_values():
    assert map_values(lambda value: value * 2,
                      {'a': 1, 'b': 2}) == {'a': 2, 'b': 4}


def is_dict():
    assert is_dict(4) == False
    assert is_dict({}) == True


def test_map_keys_by_layer():
    assert map_keys_by_layer((
        lambda first_level_key: first_level_key * 2,
        lambda second_level_key: second_level_key * 3,
        lambda third_level_key: third_level_key * 4,
    ), {1: 2, 2: 3, 3: {10: {300: 'a'}}}) == {2: 2, 4: 3, 6: {30: {1200: 'a'}}}
