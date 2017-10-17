from fptools.sequence import initial, last, chunk_by, chunk

def test_initial():
  assert initial((1, 2, 3)) == (1, 2)

def test_last():
  assert last((1, 2)) is 2

def test_chunk_by():
  assert chunk_by(lambda item, index: item % 10, (10, 20, 15, 25, 30)) == [[10, 20], [15, 25], [30]]

def test_chunk():
  assert chunk(2, (1, 2, 3, 4)) == [[1, 2], [3, 4]]
