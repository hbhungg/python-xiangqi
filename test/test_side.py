from libxiangqi import Board, IllegalMove

def test_side():
  b = Board()
  assert b.turn is True