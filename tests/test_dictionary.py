from fptools.dictionary import to_path, getitem, setitem, delitem, update, pick, omit, map_values

def test_to_path():
  assert to_path('key') == ('key',)
  assert to_path(('key',)) == ('key',)

def test_getitem():
  assert getitem('key', { 'key': 4 }) is 4
  assert getitem(('key', 'subkey'), { 'key': { 'subkey': 4 } }) is 4

def test_setitem():
  assert setitem('key', 4, {}) == { 'key': 4 }
  assert setitem(('key', 'subkey'), 4, {}) == { 'key': { 'subkey': 4 } }

def test_delitem():
  assert delitem('key', { 'key': 4 }) == {}
  assert delitem(('key', 'subkey'), { 'key': { 'subkey': 4 } }) == { 'key': {} }

def test_update():
  assert update('key', lambda value: value * 2, { 'key': 4 }) == { 'key': 8 }
  assert update(('key', 'subkey'), lambda value: value * 2, { 'key': { 'subkey': 4 } }) == { 'key': { 'subkey': 8 } }

def test_pick():
  assert pick(('foo', 'bar'), { 'foo': 4, 'bar': 2, 'yo': 3 }) == { 'foo': 4, 'bar': 2 }

def test_omit():
  assert omit(('foo', 'bar'), { 'foo': 4, 'bar': 2, 'yo': 3 }) == { 'yo': 3 }

def test_map_values():
  assert map_values(lambda value: value * 2, { 'a': 1, 'b': 2 }) == { 'a': 2, 'b': 4 }
