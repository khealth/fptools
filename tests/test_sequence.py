from fptools.sequence import initial, last

def test_initial():
  assert initial((1, 2, 3)) == (1, 2)

def test_last():
  assert last([]) is None
  assert last((1, 2)) is 2
