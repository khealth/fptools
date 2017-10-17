from iterable import head, find, avg, flatten, group_by

def test_head():
  assert head((1,)) is 1

PEOPLE = (
  { 'name': 'Alon', 'location': 'New York City' },
  { 'name': 'Lior', 'location': 'Tel Aviv' },
  { 'name': 'Ariel', 'location': 'Tel Aviv' }
)

def test_find():
  assert find(lambda person: person['name'] == 'Alon', PEOPLE) is PEOPLE[0]

def test_avg():
  assert avg((1, 2, 3)) == 2

def test_flatten():
  assert flatten((1, 2, 3, (4, 5))) == [1, 2, 3, 4, 5]

def test_group_by():
  assert group_by(lambda person: person['location'], PEOPLE) == {
    'Tel Aviv': [
      PEOPLE[1],
      PEOPLE[2]
    ],
    'New York City': [
      PEOPLE[0]
    ]
  }
