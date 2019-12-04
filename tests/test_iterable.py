from fptools.iterable import compact, head, find, find_index, mean, flatten, group_by, intersection, chunk_by, chunk, uniq, key_by


def test_compact():
    assert tuple(compact((0, 1, 2, False, True))) == (1, 2, True)


def test_head():
    assert head((1, )) is 1
    assert head(()) is None


PEOPLE = (
    {
        'name': 'Alon',
        'location': 'New York City'
    },
    {
        'name': 'Lior',
        'location': 'Tel Aviv'
    },
    {
        'name': 'Ariel',
        'location': 'Tel Aviv'
    },
    {
        'name': 'Aviv'
    }
)


def test_find():
    assert find(lambda person: person['name'] == 'Alon', PEOPLE) is PEOPLE[0]
    assert find(lambda person: person['name'] == 'Iddan', PEOPLE) is None


def test_find_index():
    assert find_index(lambda person: person['name'] == 'Alon', PEOPLE) is 0
    assert find_index(lambda person: person['name'] == 'Iddan', PEOPLE) is None


def test_mean():
    assert mean((1, 2, 3)) == 2


def test_flatten():
    assert tuple(flatten((1, 2, 3, (4, 5)))) == (1, 2, 3, 4, 5)


def test_group_by():
    assert group_by(lambda person: person.get('location'), PEOPLE) == {
        'Tel Aviv': [PEOPLE[1], PEOPLE[2]],
        'New York City': [PEOPLE[0]],
    }


def test_key_by():
    assert key_by(lambda person: person.get('location'), PEOPLE) == {
        'Tel Aviv': PEOPLE[2],
        'New York City': PEOPLE[0],
    }


def test_intersection():
    assert tuple(intersection((1, 2), (2, 3))) == (2, )


def test_chunk_by():
    assert tuple(
        chunk_by(lambda item, index: item % 10,
                 (10, 20, 15, 25, 30))) == ((10, 20), (15, 25), (30, ))


def test_chunk():
    assert tuple(chunk(2, (1, 2, 3, 4))) == ((1, 2), (3, 4))
    assert tuple(chunk(2, (1, 2, 3, 4, 5))) == ((1, 2), (3, 4), (5, ))


def test_uniq():
    assert tuple(uniq((1, 2, 3))) == (1, 2, 3)
    assert tuple(uniq((1, 2, 2, 3))) == (1, 2, 3)