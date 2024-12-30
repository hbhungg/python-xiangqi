from xiangqi import Move, Square, Board, piece_name, piece_symbol


def test_board_print():
  starting_board = """
r h e a g a e h r
. . . . . . . . .
. c . . . . . c .
s . s . s . s . s
. . . . . . . . .
. . . . . . . . .
S . S . S . S . S
. C . . . . . C .
. . . . . . . . .
R H E A G A E H R
"""
  b = Board()
  assert str(b).strip() == starting_board.strip()


def test_idk():
  from xiangqi import PieceType

  assert piece_symbol(PieceType.SOLDIER) == "s"
  assert piece_name(PieceType.SOLDIER) == "soldier"


def test_move():
  board_state = """
r h e a g a e h r
. . . . . . . . .
. c . . . . . c .
s . s . s . s . s
. . . . . . . . .
. . . . . . . . .
S . S . S . S . S
. C . . . . . C .
R . . . . . . . .
. H E A G A E H R
"""
  b = Board()
  b.push(Move(Square.A1, Square.A2))
  assert str(b).strip() == board_state.strip()
