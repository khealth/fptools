from fptools.collection import to_path, getitem, setitem, delitem, update

def test_to_path():
    assert to_path('key') == ('key',)
    assert to_path(('key',)) == ('key',)


def test_getitem():
    assert getitem('key', {'key': 4}) is 4
    assert getitem(('key', 'subkey'), {'key': {'subkey': 4}}) is 4
    assert getitem(('key'), {}) is None
    assert getitem(('key', 'subkey'), {'key': {}}) is None
    assert getitem(('key', 0), { 'key': ['item'] }) == 'item'
    assert getitem(('key', 0), { 'key': [] }) == None
    assert getitem(('key', 'subkey', 0), { 'key': { 'subkey': ['item'] } }) == 'item'
    assert getitem(('key', 0, 'subkey'), { 'key': [{ 'subkey': 'item' }] }) == 'item'


def test_setitem():
    assert setitem('key', 4, {}) == {'key': 4}
    assert setitem(('key', 'subkey'), 4, {}) == {'key': {'subkey': 4}}
    assert setitem(('key', 0), 4, {}) == {'key': [4]}
    assert setitem(('key', 1), 4, {}) == {'key': [None, 4]}
    assert setitem(('key', 1), 4, { 'key': [1, 2] }) == {'key': [1, 4]}


def test_delitem():
    assert delitem('key', {'key': 4}) == {}
    assert delitem(('key', 'subkey'), {'key': {'subkey': 4}}) == {'key': {}}


def test_update():
    assert update('key', lambda value: value * 2, {'key': 4}) == {'key': 8}
    assert update(('key', 'subkey'), lambda value: value * 2,
                  {'key': {'subkey': 4}}) == {'key': {'subkey': 8}}
